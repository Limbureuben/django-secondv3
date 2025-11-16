@echo off
REM OpenSpace Production Deployment Script for Windows
REM This script helps deploy the application

echo =========================================
echo 🚀 OpenSpace Production Deployment
echo =========================================
echo.

REM Check if .env.prod exists
if not exist .env.prod (
    echo ❌ Error: .env.prod file not found!
    echo Please create .env.prod file with your production settings.
    pause
    exit /b 1
)

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed!
    echo Please install Docker Desktop for Windows first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed!
    echo Please install Docker Compose first.
    pause
    exit /b 1
)

echo 📋 Pre-deployment checks...
echo.

REM Create necessary directories
if not exist nginx\conf.d mkdir nginx\conf.d
if not exist nginx\ssl mkdir nginx\ssl
if not exist media mkdir media
if not exist staticfiles mkdir staticfiles
if not exist backups mkdir backups

echo ✅ Pre-deployment checks passed!
echo.

echo What would you like to do?
echo 1) Fresh deployment (build and start)
echo 2) Update existing deployment (rebuild and restart)
echo 3) Start services
echo 4) Stop services
echo 5) View logs
echo 6) Create superuser
echo 7) Backup database
echo 8) Check status
echo.
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto fresh
if "%choice%"=="2" goto update
if "%choice%"=="3" goto start
if "%choice%"=="4" goto stop
if "%choice%"=="5" goto logs
if "%choice%"=="6" goto superuser
if "%choice%"=="7" goto backup
if "%choice%"=="8" goto status
goto invalid

:fresh
echo 🔨 Building production containers...
docker-compose -f docker-compose.prod.yml build
echo.
echo 🚀 Starting services...
docker-compose -f docker-compose.prod.yml up -d
echo.
echo ✅ Deployment complete!
echo.
echo Next steps:
echo 1. Create superuser: docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
echo 2. Access your app at: http://your-server-ip
echo 3. View logs: docker-compose -f docker-compose.prod.yml logs -f
goto end

:update
echo 🔄 Updating deployment...
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
echo ✅ Update complete!
goto end

:start
echo 🚀 Starting services...
docker-compose -f docker-compose.prod.yml up -d
echo ✅ Services started!
goto end

:stop
echo ⏸️  Stopping services...
docker-compose -f docker-compose.prod.yml down
echo ✅ Services stopped!
goto end

:logs
echo 📋 Viewing logs (Ctrl+C to exit)...
docker-compose -f docker-compose.prod.yml logs -f
goto end

:superuser
echo 👤 Creating superuser...
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
goto end

:backup
echo 💾 Creating database backup...
if not exist backups mkdir backups
set timestamp=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U openspace_user openspace_prod | gzip > backups\backup_%timestamp%.sql.gz
echo ✅ Backup created: backups\backup_%timestamp%.sql.gz
goto end

:status
echo 📊 Container status:
docker-compose -f docker-compose.prod.yml ps
echo.
echo 💻 Resource usage:
docker stats --no-stream
goto end

:invalid
echo ❌ Invalid choice!
goto end

:end
echo.
echo =========================================
echo Done!
echo =========================================
pause
