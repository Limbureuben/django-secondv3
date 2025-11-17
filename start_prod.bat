@echo off
echo ========================================
echo  OpenSpace Production Environment
echo ========================================

REM Check if Docker is running
docker --version >nul 2>&1
if errorlevel 1 (
    echo  Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo  Docker is running

REM Check if .env.prod exists
if not exist .env.prod (
    echo  .env.prod file not found!
    echo  Please create .env.prod file:
    echo    1. Copy .env.prod.example to .env.prod
    echo    2. Run: python generate_keys.py
    echo    3. Update .env.prod with generated keys
    pause
    exit /b 1
)

echo  .env.prod file found

REM Stop any existing containers
echo  Stopping existing containers...
docker-compose -f docker-compose.dev.yml down >nul 2>&1
docker-compose -f docker-compose.prod.yml down >nul 2>&1

REM Build and start production environment
echo  Building production environment...
docker-compose --env-file .env.prod -f docker-compose.prod.yml build

if errorlevel 1 (
    echo  Build failed. Check the output above.
    pause
    exit /b 1
)

echo  Starting production environment...
docker-compose --env-file .env.prod -f docker-compose.prod.yml up -d

if errorlevel 1 (
    echo  Failed to start containers. Check the output above.
    pause
    exit /b 1
)

REM Wait a moment for containers to start
echo  Waiting for services to start...
timeout /t 15 /nobreak >nul

REM Check container status
echo   Container Status:
docker-compose --env-file .env.prod -f docker-compose.prod.yml ps

REM Run migrations
echo  Running database migrations...
docker-compose --env-file .env.prod -f docker-compose.prod.yml exec -T web python manage.py migrate

REM Collect static files (should be automatic but ensure it's done)
echo   Collecting static files...
docker-compose --env-file .env.prod -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput

REM Security check
echo  Running security checks...
docker-compose --env-file .env.prod -f docker-compose.prod.yml exec -T web python manage.py check --deploy

echo ========================================
echo  Production environment is ready!
echo ========================================
echo   Useful commands:
echo    View logs: docker-compose -f docker-compose.prod.yml logs -f
echo    Stop:      docker-compose -f docker-compose.prod.yml down
echo    Shell:     docker-compose -f docker-compose.prod.yml exec web bash
echo.
echo   Security Notes:
echo    - Create superuser: docker-compose --env-file .env.prod -f docker-compose.prod.yml exec web python manage.py createsuperuser
echo ========================================

pause