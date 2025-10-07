from django.apps import AppConfig


class SoporteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.api.soporte'
    verbose_name = 'Sistema de Soporte'
    
    def ready(self):
        """Importar signals cuando la app esté lista."""
        import core.api.soporte.signals