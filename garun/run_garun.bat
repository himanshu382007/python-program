@echo off
title Garun AI Assistant
color 0B

echo.
echo  ===================================================
echo            Starting Garun AI Assistant
echo  ===================================================
echo.

cd /d "%~dp0"

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo [*] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [!] No virtual environment found.
    echo [*] Using system Python...
)

REM Run Garun
echo [*] Launching Garun...
echo.
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo [!] Garun exited with an error.
    pause
)
