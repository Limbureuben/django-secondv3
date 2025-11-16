#!/bin/bash

# Exit on error
set -e

echo "========================================="
echo " Starting OpenSpace Development Server"
echo "========================================="

echo " Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo " PostgreSQL is ready!"

echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.1
done
echo " Redis is ready!"

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo " Creating superuser if needed..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@openspace.dev', 'admin123')
    print(' Superuser created: admin/admin123')
else:
    print('ℹ  Superuser already exists')
END

# Collect static files
echo " Collecting static files..."
python manage.py collectstatic --noinput || true

echo "========================================="
echo " Development setup complete!"
echo " Server starting at http://localhost:8000"
echo " Admin: admin / admin123"
echo "========================================="

# Execute the main command
exec "$@"