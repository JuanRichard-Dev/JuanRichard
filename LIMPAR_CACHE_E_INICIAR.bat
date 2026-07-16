@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    set "PYTHON_CMD=.venv\Scripts\python.exe"
) else (
    set "PYTHON_CMD=python"
)

"%PYTHON_CMD%" -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Streamlit nao encontrado. Execute ATUALIZAR_DEPENDENCIAS.bat primeiro.
    pause
    exit /b 1
)

if /I "%DATA_SOURCE%"=="url" goto :source_ok
if /I "%DATA_SOURCE%"=="sharepoint" goto :source_ok
if not exist "Dashboard SM CGR 2026.xlsx" (
    echo ERRO: a planilha Dashboard SM CGR 2026.xlsx nao foi encontrada.
    pause
    exit /b 1
)
:source_ok

echo Limpando cache do Streamlit...
"%PYTHON_CMD%" -m streamlit cache clear

echo.
echo Iniciando Dashboard SM CGR 2026 V8 Deploy Ready...
"%PYTHON_CMD%" -m streamlit run app.py --server.port 8501
pause
