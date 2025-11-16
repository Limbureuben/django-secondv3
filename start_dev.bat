@echo off
echo Starting development environment...
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d
echo Development environment started!
echo Access your app at: http://localhost:8000
pause