@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Ambiente virtual nao encontrado.
    echo Execute primeiro: powershell -ExecutionPolicy Bypass -File CONFIGURAR_HOST_INTERNO.ps1
    pause
    exit /b 1
)

if not exist ".streamlit\secrets.toml" (
    echo Configuracao local nao encontrada.
    echo Execute primeiro: powershell -ExecutionPolicy Bypass -File CONFIGURAR_HOST_INTERNO.ps1
    pause
    exit /b 1
)

if not exist ".runtime\logs" mkdir ".runtime\logs"

set PYTHONUTF8=1
echo Iniciando dashboard na rede interna...
echo O acesso externo depende de firewall e autorizacao do TI.
".venv\Scripts\python.exe" -m streamlit run app.py ^
  --server.address=0.0.0.0 ^
  --server.port=8501 ^
  --server.headless=true 1>>".runtime\logs\streamlit.log" 2>>&1
