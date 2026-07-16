param(
    [string]$WorkbookPath = "$env:USERPROFILE\OneDrive - MFP Michelin\Dashboard SM CGR 2026.xlsx",
    [switch]$SkipDependencies
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

Write-Host "Dashboard SM CGR - configuracao do host interno" -ForegroundColor Cyan
Write-Host "Projeto: $ProjectRoot"

if (-not (Test-Path -LiteralPath $WorkbookPath)) {
    Write-Warning "Planilha nao encontrada no caminho informado:"
    Write-Host $WorkbookPath
    $WorkbookPath = Read-Host "Cole o caminho completo da planilha sincronizada"
}

if (-not (Test-Path -LiteralPath $WorkbookPath)) {
    throw "A planilha nao foi encontrada. Confirme a sincronizacao do OneDrive."
}

$StreamlitDir = Join-Path $ProjectRoot ".streamlit"
New-Item -ItemType Directory -Path $StreamlitDir -Force | Out-Null
$SecretsPath = Join-Path $StreamlitDir "secrets.toml"

if (Test-Path $SecretsPath) {
    Copy-Item $SecretsPath "$SecretsPath.backup-$(Get-Date -Format yyyyMMdd-HHmmss)"
}

$TomlPath = $WorkbookPath.Replace("\", "/")
@"
DATA_SOURCE = "local"
DATA_LOCAL_PATH = "$TomlPath"

AUTH_MODE = "off"
WAREHOUSE_ENABLED = false

AUTO_REFRESH_ENABLED = true
AUTO_REFRESH_SECONDS = 120
LOCAL_RUNTIME_DIR = ".runtime"
KEEP_SOURCE_SNAPSHOTS = 6
LOCAL_READ_ATTEMPTS = 8
LOCAL_READ_RETRY_SECONDS = 0.5

AUDIT_FILE_ENABLED = true
AUDIT_FILE_PATH = ".runtime/logs/audit.jsonl"
"@ | Set-Content -Path $SecretsPath -Encoding UTF8

Write-Host "Secrets locais configurados em .streamlit\secrets.toml" -ForegroundColor Green

if (-not $SkipDependencies) {
    if (-not (Test-Path ".venv\Scripts\python.exe")) {
        python -m venv .venv
    }
    & ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
    & ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
}

Write-Host ""
Write-Host "Configuracao concluida." -ForegroundColor Green
Write-Host "Execute INICIAR_LOCAL.bat para testar neste computador."
Write-Host "Execute INICIAR_REDE_INTERNA.bat somente apos a liberacao do TI."
