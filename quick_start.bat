@echo off
echo ========================================
echo Quick Start - Development Environment
echo ========================================

echo  Cleaning up Docker...
docker system prune -f
docker-compose -f docker-compose.dev.yml down --volumes

echo  Building containers (simplified)...
docker-compose -f docker-compose.dev.yml build --no-cache web

if errorlevel 1 (
    echo  Build failed. Trying alternative method...
    echo  Using standard docker-compose...
    docker-compose -f docker-compose.dev.yml up --build -d
) else (
    echo  Build successful. Starting services...
    docker-compose -f docker-compose.dev.yml up -d
)

echo  Waiting for services to start...
timeout /t 15 /nobreak >nul

echo  Container Status:
docker-compose -f docker-compose.dev.yml ps

echo  Running migrations...
docker-compose -f docker-compose.dev.yml exec -T web python manage.py migrate

echo ========================================
echo Development environment ready!
echo ========================================
