#!/bin/bash
set -e

echo "========================================="
echo " Starting OpenSpace Production"
echo "========================================="

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.3
done
echo "PostgreSQL ready!"

echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.3
done
echo "Redis ready!"

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "========================================="
echo " Entrypoint complete. Starting Gunicorn..."
echo "========================================="

# Hand over to CMD from docker-compose
exec "$@"
