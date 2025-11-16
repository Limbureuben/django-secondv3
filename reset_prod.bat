@echo off
echo Stopping and removing all production containers and volumes...
docker-compose --env-file .env.prod -f docker-compose.prod.yml down -v
echo Cleaned up! Now you can start fresh with: start_prod.bat
pause