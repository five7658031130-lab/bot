@echo off
REM Autonomous Music Bot Launcher - Windows
REM Fully self-healing, auto-installing everything

setlocal enabledelayedexpansion

title Music Bot - Autonomous Launcher
color 0A

echo.
echo ============================================================================
echo                    Music Bot Autonomous Launcher
echo ============================================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8+
    echo Download from: https://www.python.org/downloads/
    echo [IMPORTANT] Check "Add Python to PATH" during installation
    timeout /t 5
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found

REM Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip -q >nul 2>&1

REM Install requirements
echo [*] Installing dependencies...
python -m pip install -r requirements.txt -q

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    echo [*] Retrying...
    python -m pip install pyrogram==2.0.106 TgCrypto==1.2.5 yt-dlp aiohttp aiofiles psutil -q
)

echo [OK] Dependencies installed

REM Create directories
echo [*] Creating directories...
if not exist "downloads" mkdir downloads
if not exist "cache" mkdir cache
if not exist "temp" mkdir temp
if not exist "logs" mkdir logs

echo [OK] Directories ready

REM Start bot
echo.
echo ============================================================================
echo [*] Starting bot...
echo ============================================================================
echo.

python bot.py

if %errorlevel% neq 0 (
    echo [ERROR] Bot crashed
    echo Check logs/bot.log for details
)

pause
