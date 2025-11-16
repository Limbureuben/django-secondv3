@echo off
echo Checking container status...
docker-compose --env-file .env.prod -f docker-compose.prod.yml ps
echo.
echo Checking web container logs...
docker logs openspace_web_prod --tail 20
echo.
echo Testing direct connection to Django (bypass Nginx)...
curl http://localhost:8000
pause