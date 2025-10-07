from rest_framework import serializers
from core.models import Descuento, ServicioDescuento
from django.utils import timezone
import datetime

class DescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descuento
        fields = "__all__"

class ServicioDescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicioDescuento
        fields = "__all__"

    def validate(self, attrs):
        # Regla anti-solapamiento: no permitir dos descuentos EXCLUSIVOS
        # que se superpongan en el tiempo para el mismo servicio.
        # (chequeo básico con las fechas del Descuento)
        exclusivo = attrs.get("exclusivo", True)
        servicio = attrs["servicio"]
        descuento = attrs["descuento"]
        instance = getattr(self, "instance", None)

        if exclusivo:
            # normaliza ventana del descuento actual
            s1 = descuento.fecha_inicio
            e1 = descuento.fecha_fin

            qs = ServicioDescuento.objects.filter(servicio=servicio, exclusivo=True, estado=True).select_related("descuento")
            if instance:
                qs = qs.exclude(pk=instance.pk)
            for sd in qs:
                d2 = sd.descuento
                s2, e2 = d2.fecha_inicio, d2.fecha_fin

                # Considera None como -∞ / +∞ usando datetime timezone-aware
                # Usar el timezone actual de Django en lugar de UTC específico
                current_tz = timezone.get_current_timezone()
                s1_eff = s1 or timezone.make_aware(datetime.datetime.min, current_tz)  # Fecha mínima
                e1_eff = e1 or timezone.make_aware(datetime.datetime.max.replace(microsecond=0), current_tz)  # Fecha máxima
                s2_eff = s2 or timezone.make_aware(datetime.datetime.min, current_tz)  # Fecha mínima  
                e2_eff = e2 or timezone.make_aware(datetime.datetime.max.replace(microsecond=0), current_tz)  # Fecha máxima

                # Validación de solapamiento de fechas
                if s1_eff <= e2_eff and s2_eff <= e1_eff:
                    raise serializers.ValidationError(
                        "Ya existe un descuento EXCLUSIVO que se solapa en fechas para este servicio."
                    )
        return attrs