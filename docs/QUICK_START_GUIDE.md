# 🚀 Quick Start Guide - OpenSpace Django Project

## 📋 **Prerequisites**
- Python 3.11+
- Docker Desktop
- Git
- Code editor (VS Code recommended)

## 🐍 **STEP 1: Setup Virtual Environment**

### **1.1 Create Virtual Environment**
```bash
# Navigate to project directory
cd c:\Users\ANDREW\Desktop\SIDE_PROJECT\kinondoni\django-secondv3

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

# Verify activation (should show (venv) in prompt)
```

### **1.2 Install Dependencies**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### **1.3 Setup Environment Variables**
```bash
# Copy environment template
copy .env.example .env

# Edit .env file with your settings
# Use any text editor or:
notepad .env
```

## 🔧 **STEP 2: Test Without Docker (Local Development)**

### **2.1 Database Setup (SQLite)**
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Enter: username, email, password

# Collect static files
python manage.py collectstatic --noinput
```

### **2.2 Run Development Server**
```bash
# Start Django development server
python manage.py runserver

# Open browser and test:
# http://127.0.0.1:8000 - Main app
# http://127.0.0.1:8000/admin - Admin panel
# http://127.0.0.1:8000/graphql - GraphQL interface
```

### **2.3 Test Celery (Optional)**
```bash
# Terminal 1: Start Redis (if installed locally)
redis-server

# Terminal 2: Start Celery worker
celery -A openspace worker --loglevel=info

# Terminal 3: Start Celery beat
celery -A openspace beat --loglevel=info
```

## 🐳 **STEP 3: Test with Docker Development**

### **3.1 Stop Local Server**
```bash
# Stop Django server (Ctrl+C)
# Deactivate virtual environment
deactivate
```

### **3.2 Prepare Docker Environment**
```bash
# Ensure Docker Desktop is running
docker --version
docker-compose --version

# Copy development environment
copy .env.example .env.dev
# Edit .env.dev if needed
```

### **3.3 Build and Run Development Containers**
```bash
# Build development environment
docker-compose -f docker-compose.dev.yml build

# Start all services
docker-compose -f docker-compose.dev.yml up -d

# Check container status
docker-compose -f docker-compose.dev.yml ps
```

### **3.4 Setup Database in Docker**
```bash
# Run migrations
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

# Collect static files
docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic --noinput
```

### **3.5 Test Development Environment**
```bash
# Test endpoints
curl http://localhost:8000
curl http://localhost:8000/admin/

# View logs
docker-compose -f docker-compose.dev.yml logs -f web

# Access container shell
docker-compose -f docker-compose.dev.yml exec web bash
```

## 🏭 **STEP 4: Test Production Environment**

### **4.1 Generate Production Keys**
```bash
# Generate secure keys
python generate_keys.py

# Copy output and update .env.prod
copy .env.prod.example .env.prod
notepad .env.prod
# Replace placeholders with generated keys
```

### **4.2 Stop Development Environment**
```bash
# Stop development containers
docker-compose -f docker-compose.dev.yml down

# Clean up (optional)
docker system prune -f
```

### **4.3 Build and Run Production Containers**
```bash
# Build production environment
docker-compose -f docker-compose.prod.yml build

# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Check container status
docker-compose -f docker-compose.prod.yml ps
```

### **4.4 Setup Production Database**
```bash
# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Collect static files (should be automatic)
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### **4.5 Test Production Environment**
```bash
# Test endpoints (Nginx serves on port 80)
curl http://localhost
curl http://localhost/admin/
curl http://localhost/static/admin/css/base.css

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Test security headers
curl -I http://localhost
```

## 🧪 **STEP 5: Automated Testing**

### **5.1 Run Test Script**
```bash
# Activate virtual environment first
venv\Scripts\activate

# Install test dependencies
pip install requests

# Run comprehensive tests
python test_environments.py
```

### **5.2 Manual Health Checks**
```bash
# Development health check
docker-compose -f docker-compose.dev.yml exec web python manage.py check

# Production health check
docker-compose -f docker-compose.prod.yml exec web python manage.py check --deploy

# Database connection test
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell
```

## 📊 **STEP 6: Monitor and Debug**

### **6.1 View Logs**
```bash
# All services
docker-compose -f docker-compose.prod.yml logs

# Specific service
docker-compose -f docker-compose.prod.yml logs web
docker-compose -f docker-compose.prod.yml logs nginx
docker-compose -f docker-compose.prod.yml logs celery

# Follow logs in real-time
docker-compose -f docker-compose.prod.yml logs -f web
```

### **6.2 Access Services**
```bash
# Django shell
docker-compose -f docker-compose.prod.yml exec web python manage.py shell

# Database shell
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell

# Container bash
docker-compose -f docker-compose.prod.yml exec web bash

# PostgreSQL direct access
docker-compose -f docker-compose.prod.yml exec db psql -U openspace_user openspace_prod
```

### **6.3 Performance Monitoring**
```bash
# Container resource usage
docker stats

# Celery monitoring (Flower)
# Open: http://localhost/flower/

# Check container health
docker-compose -f docker-compose.prod.yml ps
```

## 🛑 **STEP 7: Stop and Clean Up**

### **7.1 Stop Services**
```bash
# Stop development
docker-compose -f docker-compose.dev.yml down

# Stop production
docker-compose -f docker-compose.prod.yml down

# Stop and remove volumes (WARNING: deletes data)
docker-compose -f docker-compose.prod.yml down -v
```

### **7.2 Clean Up Docker**
```bash
# Remove unused containers, networks, images
docker system prune -f

# Remove all volumes (WARNING: deletes all data)
docker volume prune -f

# Remove specific images
docker image rm openspace_web_prod openspace_web_dev
```

## 🔄 **STEP 8: Development Workflow**

### **8.1 Daily Development**
```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Make code changes...

# View logs
docker-compose -f docker-compose.dev.yml logs -f web

# Restart specific service after changes
docker-compose -f docker-compose.dev.yml restart web

# Stop when done
docker-compose -f docker-compose.dev.yml down
```

### **8.2 Before Deployment**
```bash
# Test production locally
docker-compose -f docker-compose.prod.yml up -d

# Run security checks
python generate_keys.py
docker-compose -f docker-compose.prod.yml exec web python manage.py check --deploy

# Test all endpoints
python test_environments.py

# Stop production test
docker-compose -f docker-compose.prod.yml down
```

## 🚨 **Troubleshooting**

### **Common Issues:**

**Port already in use:**
```bash
# Find process using port
netstat -ano | findstr :8000
# Kill process
taskkill /PID <PID> /F
```

**Container won't start:**
```bash
# Check logs
docker-compose -f docker-compose.dev.yml logs web

# Rebuild container
docker-compose -f docker-compose.dev.yml build --no-cache web
```

**Database connection error:**
```bash
# Check database container
docker-compose -f docker-compose.dev.yml ps db

# Restart database
docker-compose -f docker-compose.dev.yml restart db
```

**Permission denied:**
```bash
# Windows: Run as Administrator
# Or check Docker Desktop settings
```

**Static files not loading:**
```bash
# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Check nginx logs
docker-compose -f docker-compose.prod.yml logs nginx
```

## ✅ **Success Indicators**

### **Development Working:**
- ✅ `http://localhost:8000` shows Django app
- ✅ `http://localhost:8000/admin` shows admin login
- ✅ `http://localhost:8000/graphql` shows GraphQL interface
- ✅ All containers running: `docker-compose ps`

### **Production Working:**
- ✅ `http://localhost` shows Django app (via Nginx)
- ✅ `http://localhost/admin` shows admin login
- ✅ `http://localhost/static/admin/css/base.css` loads CSS
- ✅ Security headers present: `curl -I http://localhost`
- ✅ All containers healthy: `docker-compose ps`

## 🎉 **Next Steps**

1. **For Development:** Use `docker-compose.dev.yml` for daily coding
2. **For Production Testing:** Use `docker-compose.prod.yml` locally
3. **For Deployment:** Follow `DEPLOYMENT_STEPS.md`
4. **For Security:** Review `SECURITY_CHECKLIST.md`

Your OpenSpace Django application is now ready for development and production! 🚀