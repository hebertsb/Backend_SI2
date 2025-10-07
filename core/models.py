from django.db import models
from django.conf import settings
from decimal import Decimal
import json

USER_MODEL = settings.AUTH_USER_MODEL

# =========================
# MODELOS DE RESERVAS
# =========================

class Reserva(models.Model):
    ESTADOS = (
        ("PENDIENTE", "Pendiente"),
        ("CONFIRMADA", "Confirmada"),
        ("PAGADA", "Pagada"),
        ("CANCELADA", "Cancelada"),
        ("COMPLETADA", "Completada"),
        ("REPROGRAMADA", "Reprogramada"),
    )
    usuario = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name="reservas")
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="PENDIENTE")
    cupon = models.ForeignKey('Cupon', on_delete=models.SET_NULL, null=True, blank=True)
    detalles = models.JSONField(default=list, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.0"))
    moneda = models.CharField(max_length=10, default="BOB")
    fecha_original = models.DateTimeField(null=True, blank=True)
    fecha_reprogramacion = models.DateTimeField(null=True, blank=True)
    numero_reprogramaciones = models.IntegerField(default=0)
    motivo_reprogramacion = models.CharField(max_length=255, blank=True, null=True)
    reprogramado_por = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="reprogramaciones_realizadas")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reserva {self.id} - {self.usuario}"  # type: ignore

class Acompanante(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    documento = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telefono = models.CharField(max_length=25, null=True, blank=True)
    nacionalidad = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class ReservaAcompanante(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name="acompanantes")
    acompanante = models.ForeignKey(Acompanante, on_delete=models.CASCADE)
    relacion = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=20, default="ACTIVO")
    es_titular = models.BooleanField(default=False)

    class Meta:
        unique_together = ('reserva', 'acompanante')

    def __str__(self):
        return f"{self.acompanante} en {self.reserva}"

class ReservaServicio(models.Model):
    reserva = models.ForeignKey('Reserva', on_delete=models.CASCADE, related_name='servicios')
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.0"))
    moneda = models.CharField(max_length=10, default="BOB")

    def __str__(self):
        return f"{self.reserva} - {self.servicio}"

class HistorialReprogramacion(models.Model):
    reserva = models.ForeignKey('Reserva', on_delete=models.CASCADE, related_name='historial_reprogramaciones')
    fecha_anterior = models.DateTimeField()
    fecha_nueva = models.DateTimeField()
    motivo = models.CharField(max_length=255)
    reprogramado_por = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL, null=True)
    notificacion_enviada = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Historial {self.reserva} - {self.fecha_nueva}"

# =========================
# MODELOS DE CATALOGO
# =========================

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, default="")
    tipo = models.CharField(max_length=100)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.0"))
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="servicios")
    dias = models.IntegerField(default=1)
    descripcion_servicio = models.TextField(default="")
    incluido = models.JSONField(default=list)
    calificacion = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    visible_publico = models.BooleanField(default=True)
    imagenes = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

class Itinerario(models.Model):
    dia = models.IntegerField()
    titulo = models.CharField(max_length=255)
    actividades = models.JSONField()

    def __str__(self):
        return f"Día {self.dia}: {self.titulo}"

class Paquete(models.Model):
    nombre = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255)
    descripcion_corta = models.TextField()
    descripcion_completa = models.TextField()
    calificacion = models.DecimalField(max_digits=2, decimal_places=1)
    numero_reseñas = models.IntegerField()
    precio = models.CharField(max_length=100)
    precio_original = models.CharField(max_length=100)
    duracion = models.CharField(max_length=100)
    max_personas = models.IntegerField()
    dificultad = models.CharField(max_length=100)
    imagenes = models.JSONField()
    servicios = models.ManyToManyField(Servicio)
    itinerario = models.ManyToManyField(Itinerario, related_name="paquetes")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="paquetes", default=lambda: 1) # type: ignore
    incluido = models.JSONField()
    no_incluido = models.JSONField()
    fechas_disponibles = models.JSONField()
    descuento = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nombre

# =========================
# MODELOS DE CUPONES
# =========================

class Cupon(models.Model):
    TIPO = (("PORCENTAJE","PORCENTAJE"),("FIJO","FIJO"))
    codigo = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=12, choices=TIPO)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.0"))
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    def __str__(self): return self.codigo

# =========================
# MODELOS DE DESCUENTOS
# =========================

class Descuento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.0"))
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)
    tipo = models.CharField(max_length=12, choices=(("PORCENTAJE","PORCENTAJE"),("FIJO","FIJO")), default="PORCENTAJE")
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.0"))
    codigo = models.CharField(max_length=50, unique=True, default="")
   
    def __str__(self):
        return self.nombre

class ServicioDescuento(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    descuento = models.ForeignKey(Descuento, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField(auto_now_add=True)
    exclusivo = models.BooleanField(default=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.servicio} - {self.descuento}"

# =========================
# MODELOS DE SOPORTE
# =========================

class ConfiguracionSoporte(models.Model):
    tiempo_respuesta_critica = models.IntegerField(default=1, help_text="Horas para respuesta crítica")
    tiempo_respuesta_alta = models.IntegerField(default=4, help_text="Horas para respuesta alta")
    tiempo_respuesta_media = models.IntegerField(default=12, help_text="Horas para respuesta media")
    tiempo_respuesta_baja = models.IntegerField(default=24, help_text="Horas para respuesta baja")
    asignacion_automatica = models.BooleanField(default=True)
    max_solicitudes_por_agente = models.IntegerField(default=10)
    enviar_emails_cliente = models.BooleanField(default=True)
    enviar_emails_soporte = models.BooleanField(default=True)
    dias_auto_cierre_resueltas = models.IntegerField(default=7)
    recordatorio_cliente_dias = models.IntegerField(default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Configuración de Soporte"
    
    @classmethod
    def obtener_configuracion(cls):
        return cls.objects.first()
    

class TicketSoporte(models.Model):
    class TipoSolicitud(models.TextChoices):
        CONSULTA = 'CONSULTA', 'Consulta'
        INCIDENCIA = 'INCIDENCIA', 'Incidencia'
        REPROGRAMACION = 'REPROGRAMACION', 'Reprogramación'
        # Agrega más tipos si lo necesitas

    class EstadoSolicitud(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        EN_PROCESO = 'EN_PROCESO', 'En Proceso'
        ESPERANDO_CLIENTE = 'ESPERANDO_CLIENTE', 'Esperando Cliente'
        RESUELTO = 'RESUELTO', 'Resuelto'
        CERRADO = 'CERRADO', 'Cerrado'
        # Agrega más estados si lo necesitas

    class PrioridadSolicitud(models.TextChoices):
        BAJA = 'BAJA', 'Baja'
        MEDIA = 'MEDIA', 'Media'
        ALTA = 'ALTA', 'Alta'
        CRITICA = 'CRITICA', 'Crítica'

    usuario = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name='tickets_soporte')
    tipo_solicitud = models.CharField(max_length=20, choices=TipoSolicitud.choices, default=TipoSolicitud.CONSULTA)
    estado = models.CharField(max_length=20, choices=EstadoSolicitud.choices, default=EstadoSolicitud.PENDIENTE)
    prioridad = models.CharField(max_length=10, choices=PrioridadSolicitud.choices, default=PrioridadSolicitud.MEDIA)
    asunto = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)  
    fecha_primera_respuesta = models.DateTimeField(null=True, blank=True)  
    fecha_resolucion = models.DateTimeField(null=True, blank=True)  
    tiempo_total_resolucion = models.FloatField(null=True, blank=True)  
    satisfaccion_cliente = models.FloatField(null=True, blank=True)
    numero_ticket = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    
    def __str__(self):
        return f"Ticket {self.id} - {self.estado}"  # type: ignore

class MensajeSoporte(models.Model):
    ticket = models.ForeignKey(TicketSoporte, on_delete=models.CASCADE, related_name='mensajes')
    remitente = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    # Puedes agregar campos como es_interno, leido_por_cliente, leido_por_soporte, etc.

    def __str__(self):
        return f"Mensaje {self.id} - Ticket {self.ticket.id}"  # type: ignore

# =========================
# MODELOS DEL SEGUNDO SPRINT
# =========================

class ReglasReprogramacion(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_regla = models.CharField(max_length=50)
    aplicable_a = models.CharField(max_length=50)
    valor_numerico = models.IntegerField(null=True, blank=True)
    valor_decimal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_texto = models.TextField(null=True, blank=True)
    valor_booleano = models.BooleanField(null=True, blank=True)
    fecha_inicio_vigencia = models.DateField(null=True, blank=True)
    fecha_fin_vigencia = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    prioridad = models.IntegerField(default=0)
    mensaje_error = models.TextField(null=True, blank=True)
    condiciones_extras = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    TIPOS_REGLA = [
        ('TIEMPO_MINIMO', 'Tiempo mínimo de anticipación'),
        ('TIEMPO_MAXIMO', 'Tiempo máximo para reprogramar'),
        ('LIMITE_REPROGRAMACIONES', 'Límite de reprogramaciones'),
        ('DIAS_BLACKOUT', 'Días no permitidos'),
        ('HORAS_BLACKOUT', 'Horas no permitidas'),
        ('SERVICIOS_RESTRINGIDOS', 'Servicios restringidos'),
        # Agrega más tipos según tu lógica
    ]
    
    def obtener_valor(self):
        if self.valor_numerico is not None:
            return self.valor_numerico
        if self.valor_decimal is not None:
            return self.valor_decimal
        if self.valor_texto:
            return self.valor_texto
        if self.valor_booleano is not None:
            return self.valor_booleano
        return None
    
    @classmethod
    def obtener_valor_regla(cls, tipo_regla, rol='ALL', default=None):
        regla = cls.obtener_regla_activa(tipo_regla, rol)
        if regla:
            return regla.obtener_valor()
        return default

    @classmethod
    def obtener_regla_activa(cls, tipo_regla, rol):
        return cls.objects.filter(
            tipo_regla=tipo_regla,
            aplicable_a=rol,
            activa=True
        ).order_by('-prioridad', '-created_at').first()

    def __str__(self):
        return self.nombre

class ConfiguracionGlobalReprogramacion(models.Model):
    clave = models.CharField(max_length=100, unique=True)
    valor = models.TextField()
    tipo_valor = models.CharField(max_length=50)
    activa = models.BooleanField(default=True)
    descripcion = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def obtener_valor_tipado(self):
        tipo = self.tipo_valor.upper() if self.tipo_valor else 'STRING'
        valor = self.valor

        if tipo == 'INTEGER':
            try:
                return int(valor)
            except Exception:
                return valor
        elif tipo == 'DECIMAL':
            try:
                return float(valor)
            except Exception:
                return valor
        elif tipo == 'BOOLEAN':
            return str(valor).lower() in ['true', '1', 'yes', 'si']
        elif tipo == 'JSON':
            try:
                return json.loads(valor)
            except Exception:
                return valor
        elif tipo == 'LISTA':
            return [v.strip() for v in valor.split(',')]
        return valor

    def __str__(self):
        return self.clave

class Reprogramacion(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    nueva_fecha = models.DateTimeField()
    motivo = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=50)
    regla = models.ForeignKey(ReglasReprogramacion, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reprogramación de {self.reserva} a {self.nueva_fecha}"

class Promocion(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo_beneficio = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.0"))
    condiciones = models.TextField(blank=True, null=True)
    limite_uso = models.IntegerField(default=0)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Pago(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    usuario = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.0"))
    estado = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    transaccion_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Pago {self.id} - {self.estado}"  # type: ignore

class Comprobante(models.Model):
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='comprobantes/')
    tipo = models.CharField(max_length=20)
    fecha = models.DateTimeField(auto_now_add=True)
    codigo_validacion = models.CharField(max_length=100)

    def __str__(self):
        return f"Comprobante {self.id} - {self.tipo}"  # type: ignore

class BitacoraEvento(models.Model):
    usuario = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    entidad = models.CharField(max_length=100)
    detalles = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.fecha} - {self.accion}"

class Notificacion(models.Model):
    usuario = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificación {self.id} - {self.tipo}"  # type: ignore

class Incidencia(models.Model):
    tipo = models.CharField(max_length=50)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20)
    usuario = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Incidencia {self.id} - {self.tipo}"  # type: ignore