# 🚀 SETUP RÁPIDO - BACKEND SI2

## ⚡ CONFIGURACIÓN AUTOMÁTICA (1 COMANDO)

### Desde cero:
```powershell
git clone https://github.com/hebertsb/Backend_SI2.git
cd Backend_SI2
.\setup_automatico.ps1
```

### Si ya tienes el proyecto:
```powershell
.\setup_automatico.ps1
```

### Si aparece error de permisos:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup_automatico.ps1
```

## Opción 2: Manual paso a paso
```bash
# 1. Crear entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar base de datos
python manage.py migrate

# 4. Cargar datos iniciales
python manage.py loaddata authz/fixtures/roles_seed.json
python manage.py loaddata authz/fixtures/datos_usuarios.json
python manage.py loaddata catalogo/fixtures/categoria.json
python manage.py loaddata catalogo/fixtures/servicio.json
python manage.py loaddata descuentos/fixtures/datos_descuentos.json
python manage.py loaddata cupones/fixtures/datos_cupones.json

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Iniciar servidor
python manage.py runserver
```

## URLs importantes:
- **Admin**: http://127.0.0.1:8000/admin/
- **API Docs**: http://127.0.0.1:8000/docs/
- **API**: http://127.0.0.1:8000/api/

## 📋 Archivos de ayuda disponibles:
- `INSTRUCCIONES_COMPLETAS.txt` - Guía detallada paso a paso
- `SETUP_COMPLETO.txt` - Documentación completa del proyecto
- `setup_automatico.ps1` - Script PowerShell automático
- `setup_automatico.bat` - Script Batch para Windows

## ¿Problemas? 
Lee `INSTRUCCIONES_COMPLETAS.txt` para soluciones detalladas.

---
**Sistema de Información II - UAGRM**