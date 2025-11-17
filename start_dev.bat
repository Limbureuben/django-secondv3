@echo off
echo ========================================
echo  OpenSpace Development Environment
echo ========================================

REM Check if Docker is running
docker --version >nul 2>&1
if errorlevel 1 (
    echo  Docker is not running. Please start Docker Desktop.
    pause
    exit /b 1
)

echo  Docker is running

REM Stop any existing containers
echo  Stopping existing containers...
docker-compose --env-file .env.dev -f docker-compose.dev.yml down

REM Build and start development environment
echo  Building development environment...
docker-compose --env-file .env.dev -f docker-compose.dev.yml build

if errorlevel 1 (
    echo  Build failed. Check the output above.
    pause
    exit /b 1
)

echo  Starting development environment...
docker-compose --env-file .env.dev -f docker-compose.dev.yml up -d

if errorlevel 1 (
    echo  Failed to start containers. Check the output above.
    pause
    exit /b 1
)

REM Wait a moment for containers to start
echo  Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check container status
echo   Container Status:
docker-compose --env-file .env.dev -f docker-compose.dev.yml ps

echo ========================================
echo  Development environment is ready!
echo ========================================
echo   Useful commands:
echo    View logs: docker-compose -f docker-compose.dev.yml logs -f
echo    Stop:      docker-compose -f docker-compose.dev.yml down
echo    Shell:     docker-compose -f docker-compose.dev.yml exec web bash
echo ========================================

pause
