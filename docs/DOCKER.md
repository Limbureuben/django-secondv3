# Docker Implementation Guide

## Overview

This project uses Docker multi-stage builds to create optimized production images and a convenient development environment. The Docker setup includes PostgreSQL, Redis, Django web server, and Celery workers.

## Architecture

### Multi-Stage Dockerfile

The `Dockerfile` uses a multi-stage build strategy:

- **base**: Common dependencies and setup
- **dev**: Development stage with hot-reload support
- **prod-build**: Builds static files for production
- **prod**: Minimal production runtime image

### Services Stack

- **PostgreSQL 15**: Primary database
- **Redis 7**: Cache and Celery message broker
- **Django/Gunicorn**: Web application server
- **Celery Worker**: Background task processing
- **Celery Beat**: Scheduled task scheduler

## Building the Docker Image

### Build Production Image

```bash
docker build --target prod -t openspace:prod .
```

### Build Development Image

```bash
docker build --target dev -t openspace:dev .
```

### Build with Docker Compose

```bash
# Development
docker compose -f docker-compose.dev.yml build

# Production (Simple)
docker compose -f docker-compose.simple.yml build

# Production (Full with Nginx)
docker compose -f docker-compose.prod.yml build
```

## Running the Application

### Using Docker Compose (Recommended)

#### Development Environment

```bash
# Start all services
docker compose -f docker-compose.dev.yml up -d

# View logs
docker compose -f docker-compose.dev.yml logs -f

# Stop services
docker compose -f docker-compose.dev.yml down
```

#### Production Environment (Simple)

```bash
# Build and start all services
docker compose -f docker-compose.simple.yml up --build -d

# View logs
docker compose -f docker-compose.simple.yml logs -f web

# Stop services
docker compose -f docker-compose.simple.yml down

# Stop and remove volumes (WARNING: Deletes database!)
docker compose -f docker-compose.simple.yml down -v
```

#### Production Environment (Full with Nginx)

```bash
# Build and start all services
docker compose -f docker-compose.prod.yml up --build -d

# View logs
docker compose -f docker-compose.prod.yml logs -f

# Stop services
docker compose -f docker-compose.prod.yml down
```

### Standalone Container (Not Recommended)

If you want to run just the Django container:

```bash
# Run production image
docker run -d \
  --name openspace-prod \
  -p 8000:8000 \
  --env-file .env.prod \
  -e GUNICORN_WORKERS=2 \
  -e GUNICORN_THREADS=4 \
  openspace:prod

# View logs
docker logs -f openspace-prod

# Stop and remove
docker stop openspace-prod && docker rm openspace-prod
```

**Note**: Standalone containers require separate PostgreSQL and Redis instances.

## Environment Configuration

### Required Environment Files

- **Development**: `.env.dev`
- **Production**: `.env.prod`

### Key Environment Variables

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
POSTGRES_DB=openspace_prod
POSTGRES_USER=openspace_user
POSTGRES_PASSWORD=secure-password-here
DATABASE_HOST=db
DATABASE_PORT=5432

# Redis & Celery
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Gunicorn (Optional - defaults available)
GUNICORN_WORKERS=3
GUNICORN_THREADS=2
```

## Docker Compose Files Comparison

### `docker-compose.dev.yml`

- **Purpose**: Local development
- **Features**: Hot-reload, SQLite fallback, exposed ports, mounted source code
- **Database Port**: 5432 (exposed)
- **Web Port**: 8000 (exposed)

### `docker-compose.simple.yml`

- **Purpose**: Simple production deployment
- **Features**: PostgreSQL, Redis, Celery workers, no Nginx
- **Database Port**: 5432 (exposed)
- **Web Port**: 8000 (exposed)
- **Use Case**: Quick deployment, testing, small-scale production

### `docker-compose.prod.yml`

- **Purpose**: Full production deployment
- **Features**: Nginx reverse proxy, SSL support, Flower monitoring
- **Database Port**: 5433 (exposed)
- **Nginx Ports**: 80 (HTTP), 443 (HTTPS)
- **Use Case**: Production servers with SSL, load balancing, monitoring

## Common Commands

### Managing Containers

```bash
# View running containers
docker compose -f docker-compose.simple.yml ps

# Execute commands in running container
docker compose -f docker-compose.simple.yml exec web python manage.py migrate
docker compose -f docker-compose.simple.yml exec web python manage.py createsuperuser

# Access Django shell
docker compose -f docker-compose.simple.yml exec web python manage.py shell

# View specific service logs
docker compose -f docker-compose.simple.yml logs -f celery

# Restart a specific service
docker compose -f docker-compose.simple.yml restart web
```

### Database Operations

```bash
# Run migrations
docker compose -f docker-compose.simple.yml exec web python manage.py migrate

# Create database backup
docker compose -f docker-compose.simple.yml exec db pg_dump -U openspace_user openspace_prod > backup.sql

# Restore database backup
cat backup.sql | docker compose -f docker-compose.simple.yml exec -T db psql -U openspace_user openspace_prod

# Access PostgreSQL shell
docker compose -f docker-compose.simple.yml exec db psql -U openspace_user -d openspace_prod
```

### Cleanup

```bash
# Remove stopped containers
docker compose -f docker-compose.simple.yml down

# Remove containers and volumes (WARNING: Data loss!)
docker compose -f docker-compose.simple.yml down -v

# Remove all images
docker compose -f docker-compose.simple.yml down --rmi all

# Clean up Docker system
docker system prune -a --volumes
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker compose -f docker-compose.simple.yml logs web

# Check if database is ready
docker compose -f docker-compose.simple.yml exec db pg_isready -U openspace_user
```

### Static Files Not Loading

```bash
# Collect static files
docker compose -f docker-compose.simple.yml exec web python manage.py collectstatic --noinput
```

### Database Connection Errors

1. Ensure `.env.prod` has correct database credentials
2. Check database health: `docker compose -f docker-compose.simple.yml ps`
3. Verify `DATABASE_HOST=db` (not localhost)

### Celery Tasks Not Running

```bash
# Check Celery worker logs
docker compose -f docker-compose.simple.yml logs celery

# Check Redis connection
docker compose -f docker-compose.simple.yml exec redis redis-cli ping
```

## Performance Tuning

### Gunicorn Workers

Calculate optimal workers: `(2 x CPU cores) + 1`

```bash
# Set via environment variable
docker compose -f docker-compose.simple.yml up -d \
  -e GUNICORN_WORKERS=5 \
  -e GUNICORN_THREADS=4
```

### Database Connection Pooling

Add to `settings.py`:

```python
DATABASES['default']['CONN_MAX_AGE'] = 600  # 10 minutes
```

### Redis Memory Limit

Add to `docker-compose.simple.yml`:

```yaml
redis:
  command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
```

## Security Checklist for Production

- [ ] Change `SECRET_KEY` in `.env.prod`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Use strong PostgreSQL password
- [ ] Enable SSL/TLS (use `docker-compose.prod.yml` with Nginx)
- [ ] Set `SECURE_SSL_REDIRECT=True`
- [ ] Configure `CORS_ALLOWED_ORIGINS` with specific domains
- [ ] Never commit `.env.prod` to version control
- [ ] Use Docker secrets for sensitive data in production
- [ ] Regularly update base images and dependencies

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build --target prod -t openspace:prod .
      - name: Run tests
        run: docker run openspace:prod python manage.py test
```

## Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/settings.html)
