@echo off
title Scorpion Launcher - Setup
color 0E
echo.
echo  ========================================
echo   SCORPION LAUNCHER - Instalador v2.0
echo  ========================================
echo.

:: Check Python is installed
echo [1/4] Verificando Python...
py --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    python --version >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        color 0C
        echo.
        echo  [ERROR] Python no esta instalado.
        echo.
        echo  Descargalo desde: https://www.python.org/downloads/
        echo  IMPORTANTE: Marca "Add Python to PATH" al instalar.
        echo.
        pause
        exit /b 1
    )
)
echo  [OK] Python encontrado.

:: Install dependencies
echo.
echo [2/4] Instalando dependencias...
pip install customtkinter minecraft-launcher-lib Pillow >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo  [!] Reintentando con py -m pip...
    py -3 -m pip install customtkinter minecraft-launcher-lib Pillow >nul 2>&1
)
echo  [OK] Dependencias instaladas.

:: Create .minecraft folder if needed
echo.
echo [3/4] Preparando carpeta .minecraft...
if not exist "%APPDATA%\.minecraft" (
    mkdir "%APPDATA%\.minecraft"
    echo  [OK] Carpeta .minecraft creada.
) else (
    echo  [OK] Carpeta .minecraft ya existe.
)

:: Create desktop shortcut
echo.
echo [4/4] Creando acceso directo en el escritorio...
python create_shortcut.py 2>nul
if %ERRORLEVEL% NEQ 0 (
    py -3 create_shortcut.py 2>nul
)

echo.
echo  ========================================
echo   INSTALACION COMPLETADA!
echo  ========================================
echo.
echo  Puedes iniciar el launcher desde:
echo    - El acceso directo en el Escritorio
echo    - Doble clic en ScorpionLauncher.vbs
echo.
pause
