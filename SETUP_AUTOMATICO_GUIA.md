# 🚀 Guía de Setup Automático Ultra Simplificado

## ⚡ Proceso de 1 Minuto

### Para Nuevos Desarrolladores

```bash
# 1. Clonar proyecto
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

**🎯 ¡LISTO!** Tu backend está funcionando con datos de prueba completos.

---

## 🔄 Durante el Desarrollo

### Comando Principal (Reemplaza Todo)
```bash
# Reset completo de base de datos con datos frescos
python manage.py setup_database --reset
```

**✅ Este comando hace automáticamente:**
- Elimina base de datos anterior
- Ejecuta todas las migraciones
- Corrige problemas en fixtures
- Carga usuarios con autenticación
- Carga catálogo de servicios
- Carga reservas de prueba
- Configura sistema completo

### Variaciones del Comando
```bash
# Solo recargar datos (mantiene estructura)
python manage.py setup_database --fixtures-only

# Solo migraciones sin datos
python manage.py setup_database --no-fixtures

# Ver ayuda completa
python manage.py setup_database --help
```

---

## 📱 Datos de Prueba Incluidos

### 👥 Usuarios Listos
```
Admin:     gabriel.moreno@autonoma.edu.bo / admin123
Usuario:   juan.perez@autonoma.edu.bo / admin123
Operador:  maria.lopez@autonoma.edu.bo / admin123
Soporte:   soporte@autonoma.edu.bo / admin123
```

### 🏨 Servicios Cargados
- ✅ 10+ servicios turísticos
- ✅ Paquetes con precios
- ✅ Descuentos y cupones
- ✅ Reservas de ejemplo

### 🔐 Sistema de Autenticación
- ✅ JWT configurado
- ✅ Roles y permisos
- ✅ Endpoints protegidos

---

## 🆚 Antes vs Ahora

### ❌ Proceso Anterior (15+ comandos)
```bash
python manage.py makemigrations
python manage.py migrate
python scripts/load_initial_users.py
python scripts/load_catalog_initial.py
python scripts/load_descuentos.py
python scripts/load_paquetes.py
python scripts/load_reservas.py
python scripts/fix_reservas.py
python scripts/fix_date_formats.py
python scripts/fix_model_references.py
python scripts/add_timestamps.py
python scripts/clean_fixtures.py
# ... y más scripts individuales
```

### ✅ Proceso Actual (1 comando)
```bash
python manage.py setup_database --reset
```

**🎉 Resultado**: 95% menos comandos, 100% más confiable

---

## 🔧 Para Scripts Automatizados

### Windows PowerShell
```powershell
# El script setup_after_clone.ps1 ahora usa el comando unificado
.\scripts\setup_after_clone.ps1 -CreateVenv -InstallDeps -RunMigrations -LoadData -SkipConfirm
```

### Linux/Mac Bash
```bash
# El script setup_after_clone.sh usa automáticamente el comando unificado
./scripts/setup_after_clone.sh
```

---

## 🐛 Solución de Problemas

### Si hay errores en fixtures:
```bash
# El comando corrige automáticamente los errores comunes
python manage.py setup_database --reset
```

### Si necesitas datos frescos:
```bash
# Reset completo
python manage.py setup_database --reset
```

### Si solo quieres recargar datos:
```bash
# Mantiene estructura, recarga datos
python manage.py setup_database --fixtures-only
```

---

## 📊 Verificar que Todo Funciona

```bash
# Verificar datos cargados
python manage.py shell -c "
from core.models import *
from authz.models import *
print('=== DATOS CARGADOS ===')
print(f'Usuarios: {Usuario.objects.count()}')
print(f'Servicios: {Servicio.objects.count()}')
print(f'Reservas: {Reserva.objects.count()}')
print(f'Descuentos: {Descuento.objects.count()}')
print('=== ✅ SISTEMA LISTO ===')
"

# Iniciar servidor
python manage.py runserver

# Probar API
# http://127.0.0.1:8000/api/
# http://127.0.0.1:8000/admin/
```

---

## 🎯 Resumen para Frontend

**Para integrar con el frontend:**

1. **Setup del backend**: `python manage.py setup_database --reset`
2. **Iniciar servidor**: `python manage.py runserver`
3. **API Base URL**: `http://127.0.0.1:8000/api/`
4. **Credenciales de prueba**: Ver sección "Datos de Prueba Incluidos"
5. **Documentación de endpoints**: Ver `FRONTEND_UPDATE_GUIDE.txt`

**🚀 El sistema está listo para integrarse con cualquier frontend en minutos, no horas.**