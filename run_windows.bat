@echo off
setlocal
title Proyecto Aula V9.2 BI Institucional
cd /d "%~dp0"

echo.
echo ============================================
echo   PROYECTO AULA V9.2 - INICIO LOCAL
echo ============================================
echo Carpeta: %CD%
echo.

if not exist "app\main.py" (
  echo ERROR: No encuentro app\main.py.
  echo Extrae el ZIP completo y ejecuta este archivo desde la carpeta del proyecto.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [1/4] Creando entorno virtual...
  where py >nul 2>nul
  if not errorlevel 1 (
    py -3 -m venv .venv
  ) else (
    where python >nul 2>nul
    if not errorlevel 1 (
      python -m venv .venv
    ) else (
      echo ERROR: No se encontro Python. Instala Python 3.10 o superior y marca "Add Python to PATH".
      pause
      exit /b 1
    )
  )
)

if not exist ".venv\Scripts\python.exe" (
  echo ERROR: No se pudo crear .venv.
  echo Prueba en PowerShell: py -3 -m venv .venv
  pause
  exit /b 1
)

echo [2/4] Actualizando pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 (
  echo ERROR al actualizar pip. Revisa la conexion a Internet.
  pause
  exit /b 1
)

echo [3/4] Instalando dependencias...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo ERROR instalando dependencias. Copia el mensaje anterior para revisarlo.
  pause
  exit /b 1
)

echo [4/4] Iniciando Proyecto Aula V9.2...
echo Cuando Uvicorn indique la direccion local, abre esa direccion en tu navegador.
echo Para detener el servidor, presiona CTRL+C.
echo.
".venv\Scripts\python.exe" run_local.py
echo.
echo El servidor se ha detenido.
pause
