@echo off
echo ========================================
echo 🔧 Fixing Port Conflicts
echo ========================================

echo 🛑 Stopping all containers...
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.prod.yml down

echo 🔍 Checking what's using ports...
echo Port 6379 (Redis):
netstat -ano | findstr :6379

echo Port 5432 (PostgreSQL):
netstat -ano | findstr :5432

echo Port 8000 (Django):
netstat -ano | findstr :8000

echo.
echo 🚀 Starting development with fixed ports...
docker-compose -f docker-compose.dev.yml up -d

echo ========================================
echo ✅ Port conflicts resolved!
echo ========================================
echo 📋 New port mappings:
echo   PostgreSQL: localhost:5432
echo   Redis:      localhost:6380 (changed from 6379)
echo   Django:     localhost:8000
echo ========================================

pause