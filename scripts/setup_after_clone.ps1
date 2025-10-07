<#
PowerShell helper to create venv, install requirements, run migrations
and optionally load initial data in one command after cloning the repo.

Usage (PowerShell, run from repository root):
  # create venv, install deps, run migrations and optional data loaders
  .\scripts\setup_after_clone.ps1 -CreateVenv -InstallDeps -RunMigrations -LoadData

Parameters:
  -CreateVenv   Creates a .venv directory using python -m venv .venv
  -InstallDeps  Runs `.venv\Scripts\pip.exe install -r requirements.txt`
  -RunMigrations Runs Django migrations (`manage.py migrate --noinput`)
  -LoadData     Runs provided scripts to load JSON-based initial data
  -SkipConfirm  Skip interactive confirmations
#>

param(
    [switch]$CreateVenv,
    [switch]$InstallDeps,
    [switch]$RunMigrations,
    [switch]$LoadData,
    [switch]$SkipConfirm
)

function Confirm-Or-Exit($msg) {
    if ($SkipConfirm) { return }
    $r = Read-Host "$msg (y/N)"
    if ($r -ne 'y' -and $r -ne 'Y') { Write-Host "Aborting."; exit 1 }
}

Write-Host "Running setup_after_clone.ps1"

if ($CreateVenv) {
    Confirm-Or-Exit "Crear virtualenv .venv?"
    Write-Host "Creating virtualenv .venv..."
    python -m venv .venv
}

if ($InstallDeps) {
    Confirm-Or-Exit "Instalar dependencias desde requirements.txt?"
    Write-Host "Installing requirements..."
    .\.venv\Scripts\pip.exe install --upgrade pip
    .\.venv\Scripts\pip.exe install -r requirements.txt
}

if ($RunMigrations) {
    Confirm-Or-Exit "Ejecutar migraciones Django?"
    Write-Host "Applying Django migrations..."
    .\.venv\Scripts\python.exe manage.py migrate --noinput
}

if ($LoadData) {
    Confirm-Or-Exit "Cargar todos los fixtures automaticamente?"
    Write-Host "🔄 Ejecutando setup completo de base de datos..."
    .\.venv\Scripts\python.exe manage.py setup_database --fixtures-only
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error en setup de base de datos"
        Read-Host "Presiona Enter para continuar de todos modos..."
    }
}

Write-Host "setup_after_clone.ps1 finished."
