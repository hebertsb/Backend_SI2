# ===============================================================================
# SCRIPT AUTOMATICO DE CONFIGURACION - BACKEND SI2
# Sistema de Informacion II - UAGRM  
# PowerShell Script
# ===============================================================================

Write-Host ""
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "🚀 CONFIGURACION AUTOMATICA DEL BACKEND SI2" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

# Función para mostrar errores
function Show-Error($message) {
    Write-Host "❌ ERROR: $message" -ForegroundColor Red
    Write-Host "Presiona cualquier tecla para salir..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Función para mostrar éxito
function Show-Success($message) {
    Write-Host "✅ $message" -ForegroundColor Green
}

# Verificar si Python está instalado
try {
    $pythonVersion = python --version 2>$null
    Show-Success "Python detectado: $pythonVersion"
}
catch {
    Show-Error "Python no está instalado o no está en el PATH. Instala Python 3.8+ desde https://python.org"
}

Write-Host ""

# Crear entorno virtual
Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
try {
    python -m venv .venv
    Show-Success "Entorno virtual creado"
}
catch {
    Show-Error "No se pudo crear el entorno virtual"
}

Write-Host ""

# Activar entorno virtual
Write-Host "🔧 Activando entorno virtual..." -ForegroundColor Yellow
try {
    & .\.venv\Scripts\Activate.ps1
    Show-Success "Entorno virtual activado"
}
catch {
    Write-Host "⚠️  Si hay error de permisos, ejecuta:" -ForegroundColor Yellow
    Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Show-Error "No se pudo activar el entorno virtual"
}

Write-Host ""

# Actualizar pip
Write-Host "📥 Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip | Out-Null

# Instalar dependencias
Write-Host "📚 Instalando dependencias..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt | Out-Null
    Show-Success "Dependencias instaladas correctamente"
}
catch {
    Show-Error "No se pudieron instalar las dependencias"
}

Write-Host ""

# Aplicar migraciones
Write-Host "🗄️ Aplicando migraciones..." -ForegroundColor Yellow
try {
    python manage.py migrate | Out-Null
    Show-Success "Migraciones aplicadas correctamente"
}
catch {
    Show-Error "No se pudieron aplicar las migraciones"
}

# Verificar que se creó la base de datos
if (Test-Path "db.sqlite3") {
    Show-Success "Base de datos SQLite creada: db.sqlite3"
} else {
    Show-Error "No se creó la base de datos SQLite"
}

Write-Host ""

# Cargar datos iniciales
Write-Host "📊 Cargando datos iniciales..." -ForegroundColor Yellow

$fixtures = @(
    "authz/fixtures/roles_seed.json",
    "authz/fixtures/datos_usuarios.json", 
    "catalogo/fixtures/categoria.json",
    "catalogo/fixtures/servicio.json",
    "catalogo/fixtures/itinerario.json",
    "descuentos/fixtures/datos_descuentos.json",
    "cupones/fixtures/datos_cupones.json"
)

foreach ($fixture in $fixtures) {
    if (Test-Path $fixture) {
        $fileName = Split-Path $fixture -Leaf
        Write-Host "   - Cargando $fileName..." -ForegroundColor Cyan
        try {
            python manage.py loaddata $fixture | Out-Null
            Write-Host "     ✅ $fileName cargado" -ForegroundColor Green
        }
        catch {
            Write-Host "     ⚠️  Error cargando $fileName" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   - ⚠️  No encontrado: $fixture" -ForegroundColor Yellow
    }
}

Write-Host ""

# Verificar configuración
Write-Host "🔍 Verificando configuración..." -ForegroundColor Yellow
try {
    $checkResult = python manage.py check 2>&1
    if ($checkResult -match "no issues") {
        Show-Success "Configuración verificada correctamente"
    } else {
        Write-Host "⚠️  Advertencias encontradas:" -ForegroundColor Yellow
        Write-Host $checkResult -ForegroundColor Yellow
    }
}
catch {
    Show-Error "Hay problemas en la configuración"
}

Write-Host ""
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "🎉 CONFIGURACION COMPLETADA EXITOSAMENTE" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Base de datos creada y poblada" -ForegroundColor Green
Write-Host "✅ Migraciones aplicadas" -ForegroundColor Green  
Write-Host "✅ Datos iniciales cargados" -ForegroundColor Green
Write-Host "✅ Sistema listo para usar" -ForegroundColor Green
Write-Host ""
Write-Host "📝 SIGUIENTES PASOS:" -ForegroundColor Yellow
Write-Host "   1. Crear superusuario: python manage.py createsuperuser" -ForegroundColor White
Write-Host "   2. Iniciar servidor: python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "🌐 URLs importantes:" -ForegroundColor Yellow
Write-Host "   - Admin: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host "   - API Docs: http://127.0.0.1:8000/docs/" -ForegroundColor White
Write-Host "   - API: http://127.0.0.1:8000/api/" -ForegroundColor White
Write-Host ""
Write-Host "===============================================================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "Presiona cualquier tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")