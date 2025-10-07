# pyright: reportAttributeAccessIssue=false

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.conf import settings
from core.models import TicketSoporte, MensajeSoporte
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=TicketSoporte)
def procesar_nueva_solicitud(sender, instance, created, **kwargs):
    """
    Procesa una nueva solicitud de soporte:
    1. Asigna automáticamente un agente si está configurado
    2. Envía notificación al cliente
    3. Determina prioridad automática para reprogramaciones
    """
    if created:
        from core.models import ConfiguracionSoporte
        config = ConfiguracionSoporte.objects.first()  # O usa tu método obtener_configuracion()

        if config and config.asignacion_automatica:
            agente_disponible = obtener_agente_disponible()
            if agente_disponible:
                instance.asignar_agente(agente_disponible)
                logger.info(f"Ticket {instance.id} auto-asignado a {agente_disponible.get_full_name()}")  # type: ignore

        # Prioridad automática para reprogramaciones urgentes
        if instance.tipo_solicitud == TicketSoporte.TipoSolicitud.REPROGRAMACION and hasattr(instance, 'reserva') and instance.reserva:
            from datetime import timedelta
            from django.utils import timezone

            # Si la reserva es en menos de 24 horas, prioridad alta
            if instance.reserva.fecha_inicio <= timezone.now() + timedelta(hours=24):
                instance.prioridad = TicketSoporte.PrioridadSolicitud.ALTA
                instance.save(update_fields=['prioridad'])

        # Enviar notificación al cliente
        enviar_notificacion_nueva_solicitud(instance)

        logger.info(f"Nuevo ticket creado: {instance.id} - Tipo: {instance.tipo_solicitud}")

@receiver(post_save, sender=MensajeSoporte)
def procesar_nuevo_mensaje(sender, instance, created, **kwargs):
    """
    Procesa un nuevo mensaje:
    1. Actualiza estado del ticket si es necesario
    2. Marca mensajes como leídos automáticamente según el remitente
    """
    if created:
        ticket = instance.ticket  # Ajusta si tu campo se llama diferente
        # Si el mensaje es del cliente y el ticket estaba esperando respuesta, cambiar estado
        if hasattr(instance, 'es_del_cliente') and instance.es_del_cliente and \
           ticket.estado == TicketSoporte.EstadoSolicitud.ESPERANDO_CLIENTE:
            ticket.estado = TicketSoporte.EstadoSolicitud.EN_PROCESO
            ticket.save(update_fields=['estado'])

        # Marcar como leído por el remitente automáticamente
        if hasattr(instance, 'es_del_cliente') and instance.es_del_cliente:
            instance.leido_por_cliente = True
            instance.fecha_lectura_cliente = instance.fecha
        else:
            instance.leido_por_soporte = True
            instance.fecha_lectura_soporte = instance.fecha

        instance.save(update_fields=[
            'leido_por_cliente', 'leido_por_soporte',
            'fecha_lectura_cliente', 'fecha_lectura_soporte'
        ])

        logger.info(f"Nuevo mensaje en ticket {ticket.id} de {instance.remitente.get_full_name()}")

def obtener_agente_disponible():
    """
    Busca un agente de soporte disponible con menos carga de trabajo.
    """
    try:
        grupo_soporte = Group.objects.get(name='Soporte')
        agentes = grupo_soporte.user_set.filter(is_active=True)

        if not agentes.exists():
            logger.warning("No hay agentes de soporte disponibles")
            return None

        from core.models import ConfiguracionSoporte
        config = ConfiguracionSoporte.objects.first()  # O usa tu método obtener_configuracion()

        # Si no hay configuración, usa un valor por defecto
        max_solicitudes = config.max_solicitudes_por_agente if config else 10

        agente_menos_cargado = None
        min_solicitudes = float('inf')

        for agente in agentes:
            solicitudes_activas = agente.tickets_soporte.filter(
    estado__in=[
        TicketSoporte.EstadoSolicitud.PENDIENTE,
        TicketSoporte.EstadoSolicitud.EN_PROCESO,
        TicketSoporte.EstadoSolicitud.ESPERANDO_CLIENTE
    ]
).count()  # type: ignore
            
            if solicitudes_activas < min_solicitudes and solicitudes_activas < max_solicitudes:
                min_solicitudes = solicitudes_activas
                agente_menos_cargado = agente

        return agente_menos_cargado

    except Group.DoesNotExist:
        logger.error("Grupo 'Soporte' no existe. Crear grupo en Django Admin.")
        return None
    except Exception as e:
        logger.error(f"Error obteniendo agente disponible: {e}")
        return None

def enviar_notificacion_nueva_solicitud(ticket):
    """
    Envía notificación por email al cliente sobre la nueva solicitud.
    """
    from core.models import ConfiguracionSoporte
    config = ConfiguracionSoporte.objects.first()  # O usa tu método obtener_configuracion()

    if not config or not config.enviar_emails_cliente:
        return

    try:
        cliente = ticket.usuario  # O ticket.cliente según tu modelo
        asunto = f"Solicitud de Soporte Creada - Ticket #{ticket.id}"

        mensaje_texto = f"""
Estimado/a {cliente.get_full_name()},

Hemos recibido su solicitud de soporte exitosamente.

Detalles de la solicitud:
• Ticket: #{ticket.id}
• Tipo: {ticket.get_tipo_solicitud_display()}
• Asunto: {getattr(ticket, 'asunto', '')}
• Estado: {ticket.get_estado_display()}
• Prioridad: {ticket.get_prioridad_display()}

{f"• Reserva relacionada: {ticket.reserva}" if hasattr(ticket, 'reserva') and ticket.reserva else ""}

Nuestro equipo revisará su solicitud y le responderemos lo antes posible.

Puede hacer seguimiento de su solicitud ingresando a su panel de cliente en nuestro sistema.

Saludos cordiales,
Equipo de Soporte - Sistema UAGRM
"""

        send_mail(
            subject=asunto,
            message=mensaje_texto,
            from_email=f"Soporte UAGRM <{settings.DEFAULT_FROM_EMAIL}>",
            recipient_list=[cliente.email],
            fail_silently=False,
        )

        logger.info(f"Notificación enviada a {cliente.email} para ticket {ticket.id}")

    except Exception as e:
        logger.error(f"Error enviando notificación de nueva solicitud: {e}")

def enviar_notificacion_mensaje_cliente(mensaje):
    """
    Envía notificación al cliente cuando soporte responde.
    """
    if hasattr(mensaje, 'es_del_soporte') and mensaje.es_del_soporte and not getattr(mensaje, 'es_interno', False):
        try:
            ticket = mensaje.ticket  # Ajusta si tu campo se llama diferente
            cliente = ticket.usuario  # O ticket.cliente según tu modelo
            asunto = f"Nueva respuesta en su solicitud #{ticket.id}"

            mensaje_texto = f"""
Estimado/a {cliente.get_full_name()},

Hemos respondido a su solicitud de soporte.

Ticket: #{ticket.id}
Asunto: {getattr(ticket, 'asunto', '')}

Para ver la respuesta completa y continuar la conversación, ingrese a su panel de cliente.

Saludos cordiales,
Equipo de Soporte - Sistema UAGRM
"""

            send_mail(
                subject=asunto,
                message=mensaje_texto,
                from_email=f"Soporte UAGRM <{settings.DEFAULT_FROM_EMAIL}>",
                recipient_list=[cliente.email],
                fail_silently=False,
            )

            logger.info(f"Notificación de respuesta enviada a {cliente.email}")

        except Exception as e:
            logger.error(f"Error enviando notificación de mensaje: {e}")