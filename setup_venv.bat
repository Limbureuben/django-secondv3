@echo off
echo ========================================
echo  OpenSpace Virtual Environment Setup
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo  Python is not installed or not in PATH.
    echo  Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

echo  Python is installed
python --version

REM Check if virtual environment already exists
if exist venv (
    echo  Virtual environment already exists.
    set /p choice="Do you want to recreate it? (y/N): "
    if /i "%choice%"=="y" (
        echo  Removing existing virtual environment...
        rmdir /s /q venv
    ) else (
        echo  Using existing virtual environment.
        goto activate_venv
    )
)

REM Create virtual environment
echo  Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo  Failed to create virtual environment.
    pause
    exit /b 1
)

:activate_venv
REM Activate virtual environment
echo  Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo  Installing project dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo  Failed to install dependencies.
    echo  Make sure requirements.txt exists and is valid.
    pause
    exit /b 1
)

REM Install additional development tools
echo Installing development tools...
pip install requests python-dotenv

REM Create .env file if it doesn't exist
if not exist .env (
    echo  Creating .env file from template...
    copy .env.example .env >nul 2>&1
    if errorlevel 1 (
        echo  Could not create .env file. Please copy .env.example to .env manually.
    ) else (
        echo  .env file created. Please edit it with your settings.
    )
)

echo ========================================
echo  Virtual environment setup complete!
echo ========================================
echo  Virtual environment: venv\
echo  Dependencies installed: %cd%\requirements.txt
echo  Environment file: .env
echo.
echo  Next steps:
echo    1. Edit .env file with your settings
echo    2. Run: python manage.py migrate
echo    3. Run: python manage.py createsuperuser
echo    4. Run: python manage.py runserver
echo.
echo  To activate virtual environment manually:
echo    venv\Scripts\activate
echo.
echo  To use Docker instead:
echo    start_dev.bat    (Development)
echo    start_prod.bat   (Production)
echo ========================================

pause