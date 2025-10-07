# Sistema de Notificaciones para Reprogramación de Reservas

## Descripción General

El sistema de notificaciones para reprogramación permite enviar comunicaciones automáticas cuando se modifican las fechas de las reservas:

- **Email para clientes**: Notificación automática al email del usuario con detalles de la reprogramación
- **Notificaciones para soporte**: Alertas para el equipo administrativo sobre las reprogramaciones realizadas

> **📋 Nota Importante**: Este sistema se integra con las **[Reglas de Reprogramación](./REGLAS_REPROGRAMACION_RESERVAS.md)** que definen las políticas de negocio para permitir o denegar reprogramaciones. Las notificaciones solo se envían cuando la reprogramación cumple con todas las reglas configuradas.

## Arquitectura del Sistema

### Componentes Principales

1. **NotificacionReprogramacion**: Clase principal que maneja el envío de notificaciones
2. **Sistema de Reglas**: Motor de validación que aplica políticas de reprogramación
3. **Configuración SMTP**: Sistema de email configurado en Django settings
4. **Templates**: Plantillas HTML para emails (opcional)
5. **Logging**: Sistema de logs para rastrear el envío de notificaciones

## API del Sistema de Notificaciones

### Clase NotificacionReprogramacion

Ubicación: `reservas/notifications.py`

#### Métodos Disponibles

### 1. notificar_cliente()

Envía notificación por email al cliente sobre la reprogramación de su reserva.

**Signatura:**
```python
@staticmethod
def notificar_cliente(reserva, fecha_anterior, motivo=None)
```

**Parámetros:**
- `reserva` (Reserva): Instancia del modelo Reserva que fue reprogramada
- `fecha_anterior` (datetime): Fecha y hora original de la reserva
- `motivo` (str, opcional): Razón de la reprogramación

**Retorna:**
- `True`: Si el email se envió exitosamente
- `False`: Si hubo algún error en el envío

**Funcionalidad:**
- Construye un email personalizado con detalles de la reprogramación
- Soporta templates HTML (busca `emails/reprogramacion_cliente.html`)
- Fallback a mensaje de texto plano si no hay template
- Incluye información completa: fechas, servicios, montos, motivo

**Ejemplo de uso:**
```python
from reservas.notifications import NotificacionReprogramacion

# En el endpoint de reprogramación
resultado = NotificacionReprogramacion.notificar_cliente(
    reserva=reserva_instance,
    fecha_anterior=datetime(2024, 1, 15, 10, 0),
    motivo="Cliente solicitó cambio de fecha"
)
```

### 2. notificar_administrador()

Envía notificación a los administradores sobre una reprogramación realizada.

**Signatura:**
```python
@staticmethod
def notificar_administrador(reserva, fecha_anterior, reprogramado_por, motivo=None)
```

**Parámetros:**
- `reserva` (Reserva): Instancia del modelo Reserva reprogramada
- `fecha_anterior` (datetime): Fecha y hora original
- `reprogramado_por` (User): Usuario que realizó la reprogramación
- `motivo` (str, opcional): Razón del cambio

**Retorna:**
- `True`: Si la notificación se envió correctamente
- `False`: Si ocurrió algún error

**Funcionalidad:**
- Envía email a la lista de administradores configurada
- Incluye información detallada para auditoría
- Muestra quién realizó la reprogramación
- Lista completa de servicios afectados

### 3. enviar_recordatorio_reprogramacion()

Envía recordatorio automático antes de la nueva fecha programada.

**Signatura:**
```python
@staticmethod
def enviar_recordatorio_reprogramacion(reserva, dias_antes=1)
```

**Parámetros:**
- `reserva` (Reserva): Reserva reprogramada
- `dias_antes` (int): Días antes de la fecha para enviar recordatorio (default: 1)

**Funcionalidad:**
- Verifica si es el momento correcto para enviar el recordatorio
- Envía email de recordatorio al cliente
- Útil para sistemas de recordatorios automatizados

## Configuración de Email

### Settings Requeridos

En `backend/settings.py`:

```python
# Configuración de email para Gmail
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "tu-email@gmail.com"
EMAIL_HOST_PASSWORD = "tu-app-password"
DEFAULT_FROM_EMAIL = "noreply@sistema-reservas.com"

# Lista de emails de administradores (opcional)
ADMIN_EMAILS = [
    'admin@tuagencia.com',
    'soporte@tuagencia.com',
    'gerencia@tuagencia.com'
]
```

### Variables de Entorno

Para mayor seguridad, configurar en `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password-de-google
```

## Integración en Endpoints

### Flujo Completo con Validación de Reglas

El proceso de reprogramación incluye validación automática de reglas antes del envío de notificaciones:

```python
@action(detail=True, methods=["post"], url_path="reprogramar")
def reprogramar(self, request, pk=None):
    # 1. VALIDACIÓN DE REGLAS
    # El serializador ReprogramacionReservaSerializer valida automáticamente:
    # - Tiempo mínimo de anticipación
    # - Tiempo máximo hacia el futuro  
    # - Límite de reprogramaciones por reserva
    # - Días y horas blackout
    # - Servicios restringidos
    
    serializer = ReprogramacionReservaSerializer(
        data=request.data,
        context={'request': request, 'reserva': reserva}
    )
    
    if not serializer.is_valid():
        # Si viola alguna regla, retorna error SIN enviar notificaciones
        return Response({
            "error": "Reprogramación no permitida",
            "detalles": serializer.errors,
            "reglas_violadas": True
        }, status=400)
    
    # 2. ACTUALIZACIÓN DE LA RESERVA
    # Solo si pasa todas las validaciones de reglas
    fecha_anterior = reserva.fecha_inicio
    # ... lógica de actualización ...
    
    # 3. ENVÍO DE NOTIFICACIONES
    # Solo se ejecuta si la reprogramación fue exitosa
    notificacion_cliente = NotificacionReprogramacion.notificar_cliente(
        reserva, fecha_anterior, motivo
    )
    notificacion_admin = NotificacionReprogramacion.notificar_administrador(
        reserva, fecha_anterior, request.user, motivo
    )
    
    return Response({
        "mensaje": "Reserva reprogramada exitosamente",
        "reglas_aplicadas": True,
        "notificaciones": {
            "cliente_notificado": notificacion_cliente,
            "admin_notificado": notificacion_admin
        }
    })
```

### Integración con Sistema de Reglas

Las notificaciones se integran estrechamente con las **[Reglas de Reprogramación](./REGLAS_REPROGRAMACION_RESERVAS.md)**:

1. **Validación previa**: Las reglas se verifican antes de permitir cualquier reprogramación
2. **Mensajes contextuales**: Los emails incluyen información sobre qué reglas se aplicaron
3. **Notificaciones condicionales**: Algunas reglas pueden disparar notificaciones especiales
4. **Auditoría**: Se registra qué reglas se evaluaron para cada reprogramación

#### Ejemplo de Notificación con Información de Reglas

```python
# En el template de email para administradores
contexto = {
    'reserva': reserva,
    'reglas_aplicadas': [
        {'tipo': 'TIEMPO_MINIMO', 'valor': '24 horas', 'cumplida': True},
        {'tipo': 'LIMITE_REPROGRAMACIONES', 'valor': '3 máximo', 'cumplida': True},
        {'tipo': 'DIAS_BLACKOUT', 'valor': 'Sin fines de semana', 'cumplida': True}
    ],
    'numero_reprogramaciones': reserva.numero_reprogramaciones,
    'es_ultima_reprogramacion': reserva.numero_reprogramaciones >= limite_maximo
}
```

### Endpoint de Reprogramación

En `reservas/views.py`, las notificaciones se ejecutan automáticamente:

```python
@action(detail=True, methods=["post"], url_path="reprogramar")
def reprogramar(self, request, pk=None):
    # ... lógica de reprogramación ...
    
    # Envío de notificaciones
    notificacion_cliente = NotificacionReprogramacion.notificar_cliente(
        reserva, fecha_anterior, motivo
    )
    notificacion_admin = NotificacionReprogramacion.notificar_administrador(
        reserva, fecha_anterior, request.user, motivo
    )
    
    return Response({
        "mensaje": "Reserva reprogramada exitosamente",
        "notificaciones": {
            "cliente_notificado": notificacion_cliente,
            "admin_notificado": notificacion_admin
        }
    })
```

## Templates de Email

### Template para Cliente

Crear archivo: `templates/emails/reprogramacion_cliente.html`

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Reprogramación de Reserva</title>
</head>
<body>
    <h2>Tu reserva ha sido reprogramada</h2>
    
    <p>Hola {{ usuario.nombres }} {{ usuario.apellidos }},</p>
    
    <p>Te informamos que tu reserva #{{ reserva.pk }} ha sido reprogramada exitosamente.</p>
    
    <div style="background-color: #f5f5f5; padding: 15px; margin: 20px 0;">
        <h3>Detalles de la reprogramación:</h3>
        <ul>
            <li><strong>Fecha anterior:</strong> {{ fecha_anterior|date:"d/m/Y H:i" }}</li>
            <li><strong>Nueva fecha:</strong> {{ fecha_nueva|date:"d/m/Y H:i" }}</li>
            <li><strong>Estado:</strong> {{ reserva.estado }}</li>
            <li><strong>Total:</strong> {{ reserva.total }} {{ reserva.moneda }}</li>
        </ul>
        
        {% if motivo %}
        <p><strong>Motivo:</strong> {{ motivo }}</p>
        {% endif %}
    </div>
    
    <h4>Servicios incluidos:</h4>
    <ul>
        {% for detalle in servicios %}
        <li>{{ detalle.servicio.titulo }} (x{{ detalle.cantidad }})</li>
        {% endfor %}
    </ul>
    
    <p>Si tienes alguna pregunta, no dudes en contactarnos.</p>
    
    <p>Saludos cordiales,<br>
    Equipo de Turismo</p>
</body>
</html>
```

### Template para Administradores

Crear archivo: `templates/emails/reprogramacion_admin.html`

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Reprogramación de Reserva - Notificación Admin</title>
</head>
<body>
    <h2>Nueva reprogramación registrada</h2>
    
    <div style="background-color: #e8f4f8; padding: 15px; margin: 20px 0;">
        <h3>Información del Cliente:</h3>
        <ul>
            <li><strong>Nombre:</strong> {{ usuario.nombres }} {{ usuario.apellidos }}</li>
            <li><strong>Email:</strong> {{ usuario.email }}</li>
            <li><strong>Teléfono:</strong> {{ usuario.telefono|default:"No proporcionado" }}</li>
        </ul>
    </div>
    
    <div style="background-color: #fff3cd; padding: 15px; margin: 20px 0;">
        <h3>Detalles de la Reprogramación:</h3>
        <ul>
            <li><strong>Reserva ID:</strong> #{{ reserva.pk }}</li>
            <li><strong>Fecha anterior:</strong> {{ fecha_anterior|date:"d/m/Y H:i" }}</li>
            <li><strong>Nueva fecha:</strong> {{ fecha_nueva|date:"d/m/Y H:i" }}</li>
            <li><strong>Reprogramado por:</strong> {{ reprogramado_por.nombres }} {{ reprogramado_por.apellidos }}</li>
            <li><strong>Número de reprogramaciones:</strong> {{ reserva.numero_reprogramaciones }}</li>
            <li><strong>Total:</strong> {{ reserva.total }} {{ reserva.moneda }}</li>
        </ul>
        
        {% if motivo %}
        <p><strong>Motivo:</strong> {{ motivo }}</p>
        {% else %}
        <p><strong>Motivo:</strong> Sin motivo especificado</p>
        {% endif %}
    </div>
    
    <h4>Servicios incluidos:</h4>
    <ul>
        {% for detalle in servicios %}
        <li>{{ detalle.servicio.titulo }} (x{{ detalle.cantidad }})</li>
        {% endfor %}
    </ul>
    
    <p><strong>Acción requerida:</strong> Por favor revisa y confirma la disponibilidad para la nueva fecha.</p>
</body>
</html>
```

## Logging y Monitoreo

### Configuración de Logs

En `settings.py`, configurar logging:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/notificaciones.log',
        },
    },
    'loggers': {
        'reservas.notifications': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Mensajes de Log

El sistema registra automáticamente:

- ✅ **Éxito**: `"Notificación de reprogramación enviada al cliente {email} para reserva {id}"`
- ❌ **Error**: `"Error enviando notificación al cliente para reserva {id}: {error}"`
- ✅ **Admin**: `"Notificación de reprogramación enviada a administradores para reserva {id}"`
- 📅 **Recordatorio**: `"Recordatorio enviado para reserva reprogramada {id}"`

## Códigos de Respuesta

### Notificación Exitosa
```json
{
    "notificaciones": {
        "cliente_notificado": true,
        "admin_notificado": true
    }
}
```

### Error en Notificación
```json
{
    "notificaciones": {
        "cliente_notificado": false,
        "admin_notificado": true,
        "errores": [
            "Error enviando email al cliente: SMTP connection failed"
        ]
    }
}
```