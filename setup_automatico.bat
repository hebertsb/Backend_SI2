@echo off
REM ===============================================================================
REM SCRIPT AUTOMATICO DE CONFIGURACION - BACKEND SI2
REM Sistema de Informacion II - UAGRM
REM ===============================================================================

echo.
echo ===============================================================================
echo 🚀 CONFIGURACION AUTOMATICA DEL BACKEND SI2
echo ===============================================================================
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python detectado correctamente
echo.

REM Crear entorno virtual
echo 📦 Creando entorno virtual...
python -m venv .venv
if errorlevel 1 (
    echo ❌ ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)

echo ✅ Entorno virtual creado
echo.

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call .venv\Scripts\activate.bat

REM Actualizar pip
echo 📥 Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo 📚 Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas correctamente
echo.

REM Aplicar migraciones
echo 🗄️ Aplicando migraciones...
python manage.py migrate
if errorlevel 1 (
    echo ❌ ERROR: No se pudieron aplicar las migraciones
    pause
    exit /b 1
)

echo ✅ Migraciones aplicadas correctamente
echo.

REM Cargar datos iniciales
echo 📊 Cargando datos iniciales...

echo   - Cargando roles...
python manage.py loaddata authz/fixtures/roles_seed.json

echo   - Cargando usuarios...
python manage.py loaddata authz/fixtures/datos_usuarios.json

echo   - Cargando categorias...
python manage.py loaddata catalogo/fixtures/categoria.json

echo   - Cargando servicios...
python manage.py loaddata catalogo/fixtures/servicio.json

echo   - Cargando itinerarios...
python manage.py loaddata catalogo/fixtures/itinerario.json

echo   - Cargando descuentos...
python manage.py loaddata descuentos/fixtures/datos_descuentos.json

echo   - Cargando cupones...
python manage.py loaddata cupones/fixtures/datos_cupones.json

echo ✅ Datos iniciales cargados
echo.

REM Verificar configuracion
echo 🔍 Verificando configuracion...
python manage.py check
if errorlevel 1 (
    echo ❌ ERROR: Hay problemas en la configuracion
    pause
    exit /b 1
)

echo ✅ Configuracion verificada correctamente
echo.

echo ===============================================================================
echo 🎉 CONFIGURACION COMPLETADA EXITOSAMENTE
echo ===============================================================================
echo.
echo ✅ Base de datos creada y poblada
echo ✅ Migraciones aplicadas
echo ✅ Datos iniciales cargados
echo ✅ Sistema listo para usar
echo.
echo 📝 SIGUIENTE PASO:
echo    1. Crear superusuario: python manage.py createsuperuser
echo    2. Iniciar servidor: python manage.py runserver
echo.
echo 🌐 URLs importantes:
echo    - Admin: http://127.0.0.1:8000/admin/
echo    - API Docs: http://127.0.0.1:8000/docs/
echo    - API: http://127.0.0.1:8000/api/
echo.
echo ===============================================================================

pause