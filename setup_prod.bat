@echo off
echo ========================================
echo  Production Environment Setup
echo ========================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo  Python is not installed or not in PATH.
    echo 📥 Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

echo  Python is available

REM Check if .env.prod already exists
if exist .env.prod (
    echo  .env.prod already exists!
    set /p choice="Do you want to recreate it? (y/N): "
    if /i not "%choice%"=="y" (
        echo Using existing .env.prod file.
        echo  To update keys, delete .env.prod and run this script again.
        pause
        exit /b 0
    )
    echo  Removing existing .env.prod...
    del .env.prod
)

REM Run the Python setup script
echo  Running production setup...
python scripts\setup_production.py

if errorlevel 1 (
    echo  Setup failed. Check the output above.
    pause
    exit /b 1
)

echo ========================================
echo   Production environment setup complete!
echo ========================================
echo  Files created:
echo    .env.prod - Production environment variables
echo    production_keys_backup.txt - Backup of keys
echo.
echo   Security reminders:
echo    - Never commit .env.prod to git
echo    - Store production_keys_backup.txt securely
echo    - Update email and SMS credentials
echo.
echo  Next steps:
echo    1. Review .env.prod file
echo    2. Test: start_prod.bat
echo    3. Deploy to server
echo ========================================

pause