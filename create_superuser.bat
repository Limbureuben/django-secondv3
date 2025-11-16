@echo off
echo Creating superuser for production...
docker-compose --env-file .env.prod -f docker-compose.prod.yml exec web python manage.py createsuperuser
pause