@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    set "PYTHON_CMD=.venv\Scripts\python.exe"
) else (
    set "PYTHON_CMD=python"
)

echo Executando testes unitarios e de integracao...
"%PYTHON_CMD%" -m unittest discover -s tests -v
if errorlevel 1 (
    echo.
    echo FALHA: um ou mais testes nao passaram.
    pause
    exit /b 1
)

echo.
echo Todos os testes foram aprovados.
pause
