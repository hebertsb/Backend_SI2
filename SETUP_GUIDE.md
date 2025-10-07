# 🚀 Guía de Setup Ultra Simplificada

## ⚡ Setup Completo (Nuevo Proyecto)
```bash
# 1. Clonar repositorio
git clone https://github.com/hebertsb/Backend_SI2.git
cd Backend_SI2

# 2. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. ¡UN SOLO COMANDO PARA TODO!
python manage.py setup_database --reset

# 5. Ejecutar servidor
python manage.py runserver
```

**🎯 ¡Eso es todo!** El comando `setup_database` configura automáticamente:
- ✅ Base de datos completa con migraciones
- ✅ Usuarios de prueba con autenticación
- ✅ Catálogo de servicios turísticos  
- ✅ Reservas de ejemplo con reprogramaciones
- ✅ Sistema listo para desarrollo/producción

## 🔄 Comandos Durante Desarrollo

### 🗄️ Base de Datos (Un comando para todo)
```bash
# 🎯 COMANDO PRINCIPAL - Reset completo con todos los datos
python manage.py setup_database --reset

# Variaciones del comando unificado:
python manage.py setup_database --fixtures-only    # Solo recargar datos
python manage.py setup_database --no-fixtures      # Solo migraciones
python manage.py setup_database --help            # Ver todas las opciones

# Comandos tradicionales de Django (si los necesitas):
python manage.py showmigrations                    # Ver estado
python manage.py makemigrations                    # Crear migraciones
```

### Servidor y Testing
```bash
# Ejecutar servidor de desarrollo
python manage.py runserver

# Ejecutar tests
python manage.py test

# Crear superusuario
python manage.py createsuperuser

# Abrir shell de Django
python manage.py shell
```

### Utilidades
```bash
# Ver ayuda del comando principal
python manage.py setup_database --help

# Verificar configuración
python manage.py check

# Recolectar archivos estáticos
python manage.py collectstatic
```

## ⚡ Setup Automático con Scripts

### Windows (PowerShell)
```powershell
# Setup completo automatizado
.\scripts\setup_after_clone.ps1 -CreateVenv -InstallDeps -RunMigrations -LoadData -SkipConfirm

# Solo instalación y entorno
.\scripts\setup_after_clone.ps1 -CreateVenv -InstallDeps -SkipConfirm

# Solo configurar base de datos (usando nuevo comando)
.\scripts\setup_after_clone.ps1 -RunMigrations -LoadData -SkipConfirm
```

### Linux/Mac (Bash)
```bash
# Setup completo automatizado (usa el nuevo comando Django)
./scripts/setup_after_clone.sh
```

## 📊 Verificar Setup Exitoso

```bash
# Verificar datos cargados automáticamente
python manage.py shell -c "
from core.models import *
from authz.models import *
print('=== RESUMEN BASE DE DATOS ===')
print(f'✅ Usuarios: {Usuario.objects.count()}')
print(f'✅ Servicios: {Servicio.objects.count()}')
print(f'✅ Reservas: {Reserva.objects.count()}')
print(f'✅ Descuentos: {Descuento.objects.count()}')
print('=== SISTEMA LISTO ===')
"

# Probar servidor
python manage.py runserver
# Ir a: http://127.0.0.1:8000/api/
```

---

**🎯 Proceso Simplificado**: El comando `python manage.py setup_database --reset` reemplaza 15+ comandos anteriores. ¡Todo en uno!