# 🚀 OpenSpace - Dockerized Django Application

A fully Dockerized Django application with separate development and production configurations, ready for deployment on university servers.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Development Guide](#development-guide)
- [Production Deployment](#production-deployment)
- [Available Commands](#available-commands)

## ✨ Features

- 🐳 **Fully Dockerized** - Separate dev and production configurations
- 🔄 **Celery Integration** - Background task processing with Beat scheduler
- 📊 **PostgreSQL Database** - Production-ready relational database
- 🚀 **Redis Cache** - Fast caching and message broker
- 🔌 **WebSocket Support** - Real-time features with Django Channels
- 🎨 **GraphQL API** - Modern API with Graphene-Django
- 🔐 **JWT Authentication** - Secure authentication system
- 📧 **Email Integration** - Email notifications
- 🌐 **Nginx Reverse Proxy** - Production-ready web server
- 📱 **SMS Integration ** - Africa's Talking & Beem SMS support

## 🛠️ Tech Stack

- **Backend**: Django 5.2.8
- **API**: REST Framework + GraphQL (Graphene)
- **Database**: PostgreSQL 15
- **Cache/Queue**: Redis 7
- **Task Queue**: Celery 5.5.3
- **Web Server**: Nginx (Production)
- **ASGI**: Daphne/Channels
- **Containerization**: Docker & Docker Compose

## 📁 Project Structure

```
openspace/
├── openspace/              # Django project settings
├── myapp/                  # Main Django application
├── nginx/                  # Nginx configuration (Production)
│   ├── nginx.conf
│   └── conf.d/
│       └── default.conf
├── media/                  # User uploaded files
├── staticfiles/            # Collected static files
├── .env.dev               # Development environment variables
├── .env.prod              # Production environment variables
├── .dockerignore          # Docker ignore rules
├── Dockerfile.dev         # Development Dockerfile
├── Dockerfile.prod        # Production Dockerfile
├── docker-compose.dev.yml # Development compose file
├── docker-compose.prod.yml # Production compose file
├── entrypoint.dev.sh      # Development startup script
├── entrypoint.prod.sh     # Production startup script
├── requirements.txt       # Python dependencies
├── Makefile              # Quick commands
├── setup.sh              # Setup automation script
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker (20.10+)
- Docker Compose (2.0+)
- Git

### Option 1: Using Makefile (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/openspace.git
cd openspace

# Initial setup
make setup

# Start development environment
make dev-build
make dev-up

# View logs
make dev-logs
```

### Option 2: Using Setup Script

```bash
# Clone the repository
git clone https://github.com/yourusername/openspace.git
cd openspace

# Run setup script
chmod +x setup.sh
./setup.sh
```

### Option 3: Manual Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/openspace.git
cd openspace

# Create directories
mkdir -p nginx/conf.d nginx/ssl media staticfiles backups

# Make scripts executable
chmod +x entrypoint.dev.sh entrypoint.prod.sh

# Copy environment files
cp .env.dev.example .env.dev
cp .env.prod.example .env.prod

# Build and start development
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f
```

## 🔧 Development Guide

### Starting Development Environment

```bash
# Using Makefile
make dev-up

# Using Docker Compose directly
docker-compose -f docker-compose.dev.yml up -d
```

### Access Points

- **Django App**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
  - Username: `admin`
  - Password: `admin123`
- **GraphQL**: http://localhost:8000/graphql
- **API Docs**: http://localhost:8000/api/docs/

### Common Development Tasks

```bash
# Run migrations
make dev-migrate

# Create superuser
make dev-superuser

# Access Django shell
make dev-shell

# Access container bash
make dev-bash

# View logs
make dev-logs

# Run tests
make dev-test

# Collect static files
make dev-collectstatic

# Stop development
make dev-down
```

### Database Access

```bash
# PostgreSQL shell
make db-shell-dev

# Or directly
docker-compose -f docker-compose.dev.yml exec db psql -U postgres -d openspace
```

### Celery Monitoring

```bash
# View Celery logs
make dev-logs-celery

# Check active tasks
docker-compose -f docker-compose.dev.yml exec celery celery -A openspace inspect active

# Check registered tasks
docker-compose -f docker-compose.dev.yml exec celery celery -A openspace inspect registered
```

## 🏭 Production Deployment

### Pre-deployment Checklist

1. **Update `.env.prod` file**:
   ```bash
   # Generate new keys
   make generate-secret-key
   make generate-fernet-key
   ```

2. **Critical settings to update**:
   - `SECRET_KEY` - New random value
   - `POSTGRES_PASSWORD` - Strong password
   - `FERNET_KEY` - New encryption key
   - `ALLOWED_HOSTS` - Your domain/IP
   - `CORS_ALLOWED_ORIGINS` - Your frontend URLs
   - Email settings (SMTP)
   - SMS API keys (if using)

3. **Update Nginx configuration**:
   - Edit `nginx/conf.d/default.conf`
   - Update `server_name` with your domain

### Deployment Steps

#### 1. On Your Local Machine

```bash
# Build production image
make prod-build

# Test production build locally (optional)
make prod-up
```

#### 2. Transfer to University Server

**Option A: Using Git (Recommended)**
```bash
# On server
ssh user@university-server
cd /opt
git clone https://github.com/yourusername/openspace.git
cd openspace
```

**Option B: Using SCP**
```bash
# On local machine
tar -czf openspace.tar.gz openspace/
scp openspace.tar.gz user@university-server:/opt/

# On server
cd /opt
tar -xzf openspace.tar.gz
cd openspace
```

#### 3. On University Server

```bash
# Install Docker (if not installed)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Setup project
chmod +x setup.sh entrypoint.prod.sh entrypoint.dev.sh
./setup.sh

# Update .env.prod with production values
nano .env.prod

# Build and start
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

#### 4. Setup SSL (Recommended)

```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem
sudo chown $USER:$USER nginx/ssl/*.pem

# Uncomment SSL lines in nginx/conf.d/default.conf
nano nginx/conf.d/default.conf

# Restart Nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

#### 5. Setup Auto-start

```bash
# Create systemd service
sudo nano /etc/systemd/system/openspace.service
```

Add:
```ini
[Unit]
Description=OpenSpace Docker Compose
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/openspace
ExecStart=/usr/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

```bash
# Enable service
sudo systemctl daemon-reload
sudo systemctl enable openspace.service
sudo systemctl start openspace.service
```

#### 6. Setup Firewall

```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

## 📝 Available Commands

### Using Makefile

```bash
make help              # Show all available commands
make dev-up            # Start development
make dev-down          # Stop development
make dev-logs          # View development logs
make prod-up           # Start production
make prod-down         # Stop production
make prod-logs         # View production logs
make backup            # Backup production database
make clean             # Clean up everything
make ps                # Show running containers
```

### Using Docker Compose

**Development:**
```bash
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up -d
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml logs -f
docker-compose -f docker-compose.dev.yml exec web python manage.py <command>
```

**Production:**
```bash
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml exec web python manage.py <command>
```

## 🔄 Maintenance

### Database Backups

```bash
# Create backup
make backup

# Manual backup
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U openspace_user openspace_prod | gzip > backup.sql.gz

# Restore backup
gunzip < backup.sql.gz | docker-compose -f docker-compose.prod.yml exec -T db psql -U openspace_user openspace_prod
```

### Automated Daily Backups

Create `backup.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/opt/backups/openspace"
mkdir -p $BACKUP_DIR
cd /opt/openspace
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U openspace_user openspace_prod | gzip > $BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql.gz
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
```

Add to crontab:
```bash
chmod +x backup.sh
crontab -e
# Add: 0 2 * * * /opt/openspace/backup.sh
```

### Updating Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### Monitoring

```bash
# Container status
make ps

# Resource usage
make stats

# View logs
make prod-logs

# Specific service logs
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f celery
docker-compose -f docker-compose.prod.yml logs -f nginx

# Access Flower (Celery monitoring)
# http://your-server:5555
```

## 🐛 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Find process
sudo lsof -i :8000
# Kill or change port in docker-compose.yml
```

**2. Permission Denied**
```bash
chmod +x entrypoint.dev.sh entrypoint.prod.sh
```

**3. Database Connection Issues**
```bash
# Check database
docker-compose ps db
# Restart database
docker-compose restart db
```

**4. Static Files Not Loading**
```bash
make prod-collectstatic
```

**5. Celery Not Processing**
```bash
make prod-logs-celery
docker-compose restart celery celery-beat
```

**6. Clean Start**
```bash
make clean
make dev-build
make dev-up
```

### Getting Help

```bash
# Check container logs
docker-compose logs <service-name>

# Access container shell
docker-compose exec <service-name> bash

# Check container status
docker-compose ps

# Inspect container
docker inspect <container-name>
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Graphene-Django](https://docs.graphene-python.org/projects/django/)

