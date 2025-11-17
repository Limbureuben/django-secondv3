@echo off
echo ========================================
echo Production Database Access
echo ========================================

REM Check if .env.prod exists
if not exist .env.prod (
    echo .env.prod file not found!
    echo  Please run setup_prod.bat first
    pause
    exit /b 1
)

echo  .env.prod file found

REM Check if production containers are running
docker-compose --env-file .env.prod -f docker-compose.prod.yml ps | findstr "openspace_db_prod" >nul
if errorlevel 1 (
    echo Production database container not running
    echo  Start production first: start_prod.bat
    pause
    exit /b 1
)

echo  Production database is running

echo ========================================
echo  Database Access Options:
echo ========================================
echo 1. PostgreSQL Shell (psql)
echo 2. Django Database Shell
echo 3. Show Connection Info
echo 4. Create Backup
echo ========================================

set /p choice="Choose option (1-4): "

if "%choice%"=="1" (
    echo  Accessing PostgreSQL shell...
    docker-compose --env-file .env.prod -f docker-compose.prod.yml exec db psql -U openspace_user openspace_prod
) else if "%choice%"=="2" (
    echo  Accessing Django database shell...
    docker-compose --env-file .env.prod -f docker-compose.prod.yml exec web python manage.py dbshell
) else if "%choice%"=="3" (
    echo Database Connection Info:
    python scripts\db_access.py
) else if "%choice%"=="4" (
    echo Creating database backup...
    python scripts\db_access.py backup
) else (
    echo  Invalid choice
)

pause