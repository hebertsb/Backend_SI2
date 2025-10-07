from django.contrib import admin
from core.models import Descuento

@admin.register(Descuento)
class DescuentoAdmin(admin.ModelAdmin):
    list_display = ('codigo','tipo','valor','fecha_inicio','fecha_fin','activo')
    list_filter = ('tipo','activo')
    search_fields = ('codigo',)
