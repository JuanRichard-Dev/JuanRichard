$ErrorActionPreference = "Continue"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

Write-Host "DIAGNOSTICO DO HOST INTERNO" -ForegroundColor Cyan
Write-Host "Projeto: $ProjectRoot"
Write-Host ""

$SecretsPath = Join-Path $ProjectRoot ".streamlit\secrets.toml"
if (-not (Test-Path $SecretsPath)) {
    Write-Host "[ERRO] .streamlit\secrets.toml nao encontrado." -ForegroundColor Red
} else {
    Write-Host "[OK] secrets.toml encontrado." -ForegroundColor Green
    $Text = Get-Content $SecretsPath -Raw
    $Match = [regex]::Match($Text, 'DATA_LOCAL_PATH\s*=\s*"([^"]+)"')
    if ($Match.Success) {
        $WorkbookPath = $Match.Groups[1].Value.Replace("/", "\")
        Write-Host "Planilha: $WorkbookPath"
        if (Test-Path -LiteralPath $WorkbookPath) {
            $File = Get-Item -LiteralPath $WorkbookPath
            Write-Host "[OK] Planilha acessivel." -ForegroundColor Green
            Write-Host "Tamanho: $($File.Length) bytes"
            Write-Host "Modificacao: $($File.LastWriteTime)"
        } else {
            Write-Host "[ERRO] Planilha nao encontrada." -ForegroundColor Red
        }
    }
}

if (Get-Process OneDrive -ErrorAction SilentlyContinue) {
    Write-Host "[OK] OneDrive em execucao." -ForegroundColor Green
} else {
    Write-Host "[AVISO] Processo OneDrive nao encontrado." -ForegroundColor Yellow
}

if (Test-Path ".venv\Scripts\python.exe") {
    Write-Host "[OK] Ambiente virtual encontrado." -ForegroundColor Green
    & ".\.venv\Scripts\python.exe" --version
} else {
    Write-Host "[ERRO] Ambiente virtual nao encontrado." -ForegroundColor Red
}

$Port = Get-NetTCPConnection -LocalPort 8501 -State Listen -ErrorAction SilentlyContinue
if ($Port) {
    Write-Host "[OK] Porta 8501 em escuta." -ForegroundColor Green
    try {
        $Health = Invoke-WebRequest "http://127.0.0.1:8501/_stcore/health" -UseBasicParsing -TimeoutSec 5
        Write-Host "[OK] Health check: $($Health.StatusCode)" -ForegroundColor Green
    } catch {
        Write-Host "[AVISO] Porta aberta, mas health check falhou: $($_.Exception.Message)" -ForegroundColor Yellow
    }
} else {
    Write-Host "[INFO] Dashboard nao esta em execucao na porta 8501."
}

Write-Host ""
Write-Host "Nome do computador: $env:COMPUTERNAME"
try {
    $IPv4 = Get-NetIPAddress -AddressFamily IPv4 |
        Where-Object { $_.IPAddress -notlike "169.254*" -and $_.IPAddress -ne "127.0.0.1" } |
        Select-Object -ExpandProperty IPAddress
    Write-Host "IPs internos: $($IPv4 -join ', ')"
} catch {
    Write-Host "Nao foi possivel listar os IPs."
}
