"""
Comando Django personalizado para realizar setup completo de la base de datos.
Ejecuta migraciones y carga fixtures automáticamente con todas las correcciones necesarias.

Uso:
    python manage.py setup_database
    python manage.py setup_database --reset    # Limpia y recrea todo
    python manage.py setup_database --fixtures-only  # Solo carga fixtures
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db import transaction
from django.apps import apps


class Command(BaseCommand):
    help = 'Ejecuta migraciones y carga fixtures automáticamente con correcciones'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Limpia completamente la base de datos antes de cargar datos',
        )
        parser.add_argument(
            '--fixtures-only',
            action='store_true',
            help='Solo carga fixtures, omite migraciones',
        )
        parser.add_argument(
            '--no-fixtures',
            action='store_true',
            help='Solo ejecuta migraciones, omite fixtures',
        )

    def handle(self, *args, **options):
        """Ejecuta el proceso completo de setup de base de datos."""
        self.stdout.write(
            self.style.SUCCESS('🚀 INICIANDO SETUP COMPLETO DE BASE DE DATOS')
        )
        self.stdout.write('=' * 60)

        try:
            # 1. Resetear base de datos si se solicita
            if options['reset']:
                self._reset_database()

            # 2. Ejecutar migraciones
            if not options['fixtures_only']:
                self._run_migrations()

            # 3. Cargar fixtures
            if not options['no_fixtures']:
                self._load_fixtures()

            # 4. Mostrar resumen
            self._show_summary()

            self.stdout.write(
                self.style.SUCCESS('\n🎉 ¡SETUP COMPLETADO EXITOSAMENTE!')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Error durante el setup: {e}')
            )
            raise CommandError(f'Setup falló: {e}')

    def _reset_database(self):
        """Limpia completamente la base de datos."""
        self.stdout.write('\n🔄 Reseteando base de datos...')
        try:
            call_command('flush', '--noinput')
            self.stdout.write(self.style.SUCCESS('✅ Base de datos limpiada'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️  Error limpiando: {e}'))

    def _run_migrations(self):
        """Ejecuta las migraciones de Django."""
        self.stdout.write('\n🔄 Ejecutando migraciones...')
        try:
            call_command('migrate', '--noinput')
            self.stdout.write(self.style.SUCCESS('✅ Migraciones completadas'))
        except Exception as e:
            raise CommandError(f'Error en migraciones: {e}')

    def _load_fixtures(self):
        """Carga todos los fixtures con correcciones automáticas."""
        self.stdout.write('\n🔄 Procesando y cargando fixtures...')
        
        # Aplicar correcciones automáticas
        self._fix_all_fixtures()
        
        # Cargar fixtures en orden correcto
        fixtures_order = [
            ('authz/fixtures/roles_seed.json', 'Roles'),
            ('authz/fixtures/datos_usuarios.json', 'Usuarios'),
            ('catalogo/fixtures/categoria.json', 'Categorías'),
            ('catalogo/fixtures/servicio.json', 'Servicios'),
            ('catalogo/fixtures/paquete.json', 'Paquetes'),
            ('catalogo/fixtures/itinerario.json', 'Itinerarios'),
            ('cupones/fixtures/datos_cupones.json', 'Cupones'),
            ('descuentos/fixtures/datos_descuentos.json', 'Descuentos'),
            ('reservas/fixtures/configuracion_global_inicial.json', 'Configuración Global'),
            ('reservas/fixtures/reglas_reprogramacion_inicial.json', 'Reglas de Reprogramación'),
            ('reservas/fixtures/datos_reserva.json', 'Reservas'),
        ]

        for fixture_path, description in fixtures_order:
            self._load_single_fixture(fixture_path, description)

    def _fix_all_fixtures(self):
        """Aplica todas las correcciones necesarias a los fixtures."""
        self.stdout.write('  🔧 Aplicando correcciones automáticas...')
        
        base_dir = Path(__file__).parent.parent.parent.parent
        fixtures_paths = []
        
        # Buscar todos los fixtures
        for app_dir in base_dir.glob('*/fixtures/'):
            fixtures_paths.extend(app_dir.glob('*.json'))
        
        for fixture_path in fixtures_paths:
            self._fix_single_fixture(fixture_path)
            
        self.stdout.write('  ✅ Correcciones aplicadas')

    def _fix_single_fixture(self, fixture_path):
        """Aplica todas las correcciones a un fixture individual."""
        try:
            with open(fixture_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            changes = 0
            
            for item in data:
                if 'model' in item and 'fields' in item:
                    # 1. Limpiar campos obsoletos
                    changes += self._clean_obsolete_fields(item)
                    
                    # 2. Actualizar referencias de modelos
                    changes += self._update_model_references(item)
                    
                    # 3. Corregir formatos de fecha
                    changes += self._fix_date_formats(item)
                    
                    # 4. Corregir campos de acompañantes
                    changes += self._fix_acompanante_fields(item)
                    
                    # 5. Agregar fechas faltantes a reservas
                    changes += self._fix_reserva_dates(item)
                    
                    # 6. Agregar timestamps
                    changes += self._add_timestamps(item)
            
            # Guardar cambios si hubo modificaciones
            if changes > 0:
                with open(fixture_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    
        except Exception as e:
            self.stdout.write(f'  ⚠️  Error procesando {fixture_path}: {e}')

    def _clean_obsolete_fields(self, item):
        """Remueve campos obsoletos."""
        obsolete_fields = ['created_at', 'updated_at', 'timestamp', 'estado', 'prioridad', 'fecha_servicio']
        changes = 0
        
        for field in obsolete_fields:
            if field in item['fields']:
                # Solo remover si no es un modelo que necesita timestamps
                if not self._needs_timestamps(item['model']):
                    del item['fields'][field]
                    changes += 1
                    
        return changes

    def _update_model_references(self, item):
        """Actualiza referencias de modelos que fueron movidos a core."""
        model_mapping = {
            'cupones.cupon': 'core.cupon',
            'descuentos.descuento': 'core.descuento',
            'reservas.reserva': 'core.reserva',
            'reservas.configuracionglobal': 'core.configuracionglobal',
            'reservas.reglareprogramacion': 'core.reglareprogramacion',
            'catalogo.servicio': 'core.servicio',
            'catalogo.categoria': 'core.categoria',
            'catalogo.paquete': 'core.paquete',
            'catalogo.itinerario': 'core.itinerario',
        }
        
        if item['model'] in model_mapping:
            item['model'] = model_mapping[item['model']]
            return 1
        return 0

    def _fix_date_formats(self, item):
        """Convierte DateTimeField a DateField donde sea necesario."""
        if item['model'] == 'core.descuento':
            changes = 0
            for field in ['fecha_inicio', 'fecha_fin']:
                if field in item['fields']:
                    value = item['fields'][field]
                    if isinstance(value, str) and 'T' in value:
                        item['fields'][field] = value.split('T')[0]
                        changes += 1
            return changes
        return 0

    def _fix_acompanante_fields(self, item):
        """Corrige campos de acompañantes (nombre -> nombres, apellido -> apellidos)."""
        if item['model'] == 'core.acompanante':
            changes = 0
            if 'nombre' in item['fields']:
                item['fields']['nombres'] = item['fields'].pop('nombre')
                changes += 1
            if 'apellido' in item['fields']:
                item['fields']['apellidos'] = item['fields'].pop('apellido')
                changes += 1
            return changes
        return 0

    def _fix_reserva_dates(self, item):
        """Agrega fecha_fin y estado a reservas."""
        if item['model'] == 'core.reserva':
            changes = 0
            if 'fecha_fin' not in item['fields'] and 'fecha_inicio' in item['fields']:
                try:
                    fecha_inicio_str = item['fields']['fecha_inicio']
                    if fecha_inicio_str.endswith('Z'):
                        fecha_inicio = datetime.fromisoformat(fecha_inicio_str[:-1])
                    else:
                        fecha_inicio = datetime.fromisoformat(fecha_inicio_str)
                    
                    fecha_fin = fecha_inicio + timedelta(days=3)
                    item['fields']['fecha_fin'] = fecha_fin.strftime('%Y-%m-%dT%H:%M:%SZ')
                    changes += 1
                except:
                    pass
                    
            if 'estado' not in item['fields']:
                item['fields']['estado'] = 'PENDIENTE'
                changes += 1
                
            return changes
        return 0

    def _add_timestamps(self, item):
        """Agrega timestamps requeridos a modelos que los necesitan."""
        if self._needs_timestamps(item['model']):
            changes = 0
            timestamp = "2025-01-15T10:00:00Z"
            
            for field in ['created_at', 'updated_at']:
                if field not in item['fields']:
                    item['fields'][field] = timestamp
                    changes += 1
                    
            return changes
        return 0

    def _needs_timestamps(self, model_name):
        """Determina si un modelo necesita timestamps."""
        models_with_timestamps = {
            'core.configuracionglobalreprogramacion',
            'core.reglasreprogramacion', 
            'core.reserva',
            'authz.rol',
            'core.servicio'
        }
        return model_name in models_with_timestamps

    def _load_single_fixture(self, fixture_path, description):
        """Carga un fixture individual."""
        try:
            call_command('loaddata', fixture_path)
            self.stdout.write(f'  ✅ {description} cargado')
        except Exception as e:
            self.stdout.write(f'  ❌ {description} falló: {str(e)[:100]}...')

    def _show_summary(self):
        """Muestra resumen de datos cargados."""
        self.stdout.write('\n📊 RESUMEN DE DATOS CARGADOS:')
        self.stdout.write('-' * 40)
        
        try:
            # Importar modelos dinámicamente
            from authz.models import Usuario, Rol
            from core.models import (
                Categoria, Servicio, Paquete, 
                Itinerario, Cupon, Descuento, Reserva, Acompanante,
                ConfiguracionGlobalReprogramacion, ReglasReprogramacion
            )
            
            models_data = [
                ('Usuarios', Usuario),
                ('Roles', Rol),
                ('Categorías', Categoria),
                ('Servicios', Servicio),
                ('Paquetes', Paquete),
                ('Itinerarios', Itinerario),
                ('Cupones', Cupon),
                ('Descuentos', Descuento),
                ('Reservas', Reserva),
                ('Acompañantes', Acompanante),
                ('Configuración Global', ConfiguracionGlobalReprogramacion),
                ('Reglas Reprogramación', ReglasReprogramacion),
            ]
            
            for name, model in models_data:
                try:
                    count = model.objects.count()
                    status = '✅' if count > 0 else '❌'
                    self.stdout.write(f'{status} {name}: {count} registros')
                except Exception as e:
                    self.stdout.write(f'❓ {name}: Error obteniendo datos')
                    
        except ImportError as e:
            self.stdout.write(f'⚠️  No se pudieron cargar los modelos: {e}')