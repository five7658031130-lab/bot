@echo off
REM Clean and Setup Script for Windows
REM Removes old cache, logs, and dependencies

setlocal enabledelayedexpansion

title Music Bot - Cleanup & Setup

echo.
echo ================================================================================
echo                         MUSIC BOT - CLEANUP SCRIPT
echo ================================================================================
echo.

REM Check if running as admin (optional but recommended)
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Not running as Administrator
    echo Some operations may be skipped
    echo.
)

REM Ask for confirmation
echo This script will:
echo - Remove cache files
echo - Remove temporary files
echo - Remove old logs
echo - Clean Python cache
echo - Remove old dependencies
echo.
set /p "confirm=Continue? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo [*] Starting cleanup...

REM Remove directories
if exist "cache" (
    echo [*] Removing cache...
    rmdir /s /q cache >nul 2>&1
    mkdir cache
    echo [OK] Cache cleared
)

if exist "temp" (
    echo [*] Removing temp files...
    rmdir /s /q temp >nul 2>&1
    mkdir temp
    echo [OK] Temp cleared
)

if exist "downloads" (
    echo [*] Removing downloads...
    rmdir /s /q downloads >nul 2>&1
    mkdir downloads
    echo [OK] Downloads cleared
)

if exist "logs" (
    echo [*] Removing logs...
    rmdir /s /q logs >nul 2>&1
    mkdir logs
    echo [OK] Logs cleared
)

REM Remove Python cache
if exist "__pycache__" (
    echo [*] Removing Python cache...
    rmdir /s /q __pycache__ >nul 2>&1
    echo [OK] Cache removed
)

if exist "plugins\__pycache__" (
    rmdir /s /q plugins\__pycache__ >nul 2>&1
    echo [OK] Plugin cache removed
)

REM Remove session files (optional)
set /p "removesession=Remove session files? (Y/N): "
if /i "%removesession%"=="Y" (
    echo [*] Removing session files...
    del /q *.session >nul 2>&1
    del /q *.session-journal >nul 2>&1
    echo [OK] Session files removed
)

REM Update pip
echo.
echo [*] Updating pip...
python -m pip install --upgrade pip >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] pip updated
) else (
    echo [WARNING] pip update failed
)

REM Reinstall requirements
echo [*] Reinstalling dependencies...
python -m pip install -r requirements.txt --force-reinstall --no-cache-dir >nul 2>&1

if %errorlevel% equ 0 (
    echo [OK] Dependencies installed
) else (
    echo [ERROR] Failed to install dependencies
)

echo.
echo ================================================================================
echo [OK] Cleanup completed!
echo ================================================================================
echo.

pause
