from django.contrib import admin
from core.models import TicketSoporte, MensajeSoporte, ConfiguracionSoporte

@admin.register(TicketSoporte)
class TicketSoporteAdmin(admin.ModelAdmin):
    list_display = ['numero_ticket', 'usuario', 'asunto', 'tipo_solicitud', 'estado', 'prioridad', 'fecha_creacion']
    list_filter = ['tipo_solicitud', 'estado', 'prioridad', 'fecha_creacion']
    search_fields = ['numero_ticket', 'asunto', 'descripcion', 'usuario__username', 'usuario__email']
    readonly_fields = ['numero_ticket', 'fecha_creacion', 'updated_at', 'fecha_primera_respuesta', 'fecha_resolucion']

@admin.register(MensajeSoporte)
class MensajeSoporteAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'remitente', 'fecha']
    list_filter = ['fecha', 'ticket__tipo_solicitud', 'ticket__estado']
    search_fields = ['mensaje', 'ticket__numero_ticket', 'remitente__username', 'remitente__email']
    readonly_fields = ['fecha']

@admin.register(ConfiguracionSoporte)
class ConfiguracionSoporteAdmin(admin.ModelAdmin):
    list_display = ['tiempo_respuesta_critica', 'tiempo_respuesta_alta', 'tiempo_respuesta_media', 'tiempo_respuesta_baja', 'asignacion_automatica']
