# 🚀 OpenSpace - Dockerized Django Application

A fully Dockerized Django application with separate development and production configurations, ready for deployment on university servers.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)


##  Features

-  **Fully Dockerized** - Separate dev and production configurations
-  **Celery Integration** - Background task processing with Beat scheduler
-  **PostgreSQL Database** - Production-ready relational database
-  **Redis Cache** - Fast caching and message broker
-  **WebSocket Support** - Real-time features with Django Channels
- **GraphQL API** - Modern API with Graphene-Django
-  **JWT Authentication** - Secure authentication system
-  **Email Integration** - Email notifications
-  **Nginx Reverse Proxy** - Production-ready web server
-  ** SMS Integration and USSD Intergration ** - Africa's Talking & Beem SMS support

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

### Option 2: Using Setup Script

```bash
# Clone the repository
git clone https://github.com/yourusername/openspace.git
cd openspace

```bash
# Clone the repository
git clone https://github.com/yourusername/openspace.git
cd openspace

cp .env.prod.example .env.prod  ##for porduction environemnt variables
cp .env.dev.example  .env.dev  ##for development environment variables

### Pre-deployment Checklist
1. **Update `.env.prod` file**:
   ```bash
   # Generate new keys
   cd scripts/
   Run python generate_keys.py
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
   - 



   How to run both development and production containers in server
   - access the server to the IP Address
   - navigate to cd /var/www/
   - navigate to cd django-secondv3
   - run docker ps to see the container running
   - run these commands below to test development and production
   - development: docker compose -f docker-compose.dev.yml up -d --build
   - Production: docker compose -f docker-compose.prod.yml up -d --build
   - To quite the containers for development or production use the below command
   - For development: docker compose -f docker-compose.dev.yml down -v or For production: docker compose -f docker-compose.prod.yml down -v
   - To see containers running run the below command
   - docker ps

