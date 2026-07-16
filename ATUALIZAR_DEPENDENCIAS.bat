@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_CMD=python"
where py >nul 2>&1 && set "PYTHON_CMD=py -3"

if not exist ".venv\Scripts\python.exe" (
    echo Criando ambiente virtual .venv...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 goto :error
)

set "VENV_PY=.venv\Scripts\python.exe"
echo Atualizando pip...
"%VENV_PY%" -m pip install --upgrade pip
if errorlevel 1 goto :error

echo Instalando dependencias do projeto...
"%VENV_PY%" -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo Dependencias instaladas com sucesso.
pause
exit /b 0

:error
echo.
echo FALHA ao preparar o ambiente Python.
pause
exit /b 1
