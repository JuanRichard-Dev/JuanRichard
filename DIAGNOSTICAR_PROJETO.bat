@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    set "PYTHON_CMD=.venv\Scripts\python.exe"
) else (
    set "PYTHON_CMD=python"
)

"%PYTHON_CMD%" diagnostico_projeto.py
set "EXIT_CODE=%ERRORLEVEL%"
echo.
if "%EXIT_CODE%"=="0" (
    echo Diagnostico concluido sem divergencias criticas.
) else (
    echo Diagnostico encontrou erros ou divergencias. Revise a saida acima.
)
pause
exit /b %EXIT_CODE%
