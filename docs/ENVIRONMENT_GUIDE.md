# 🎯 Environment Management Guide

## 🏆 **Best Solution Implemented**

Your project now uses **Smart Environment Detection** that automatically:
- ✅ Detects environment (local/development/production)
- ✅ Loads correct .env file
- ✅ Applies environment-specific settings
- ✅ Enforces security in production
- ✅ Works with Docker and local development

## 🔍 **How It Works**

### **Environment Detection Logic:**
```python
def detect_environment():
    # 1. Check DJANGO_ENVIRONMENT variable (highest priority)
    if os.getenv('DJANGO_ENVIRONMENT'):
        return 'production' or 'development'
    
    # 2. Auto-detect production (DB_HOST=db + DEBUG=False)
    if os.getenv('DB_HOST') == 'db' and os.getenv('DEBUG') == 'False':
        return 'production'
    
    # 3. Auto-detect development (.env.dev exists)
    elif os.path.exists('.env.dev'):
        return 'development'
    
    # 4. Default to local
    else:
        return 'local'
```

### **File Loading Priority:**
1. **Production**: `.env.prod`
2. **Development**: `.env.dev` 
3. **Local**: `.env`

## 🚀 **Usage Examples**

### **1. Local Development (SQLite)**
```bash
# No Docker, uses SQLite
python manage.py runserver
# → Environment: local
# → Database: SQLite
# → Debug: True
# → CORS: Allow all
```

### **2. Docker Development (PostgreSQL)**
```bash
# Uses docker-compose.dev.yml
start_dev.bat
# → Environment: development
# → Database: PostgreSQL
# → Debug: True
# → CORS: Allow all
```

### **3. Docker Production**
```bash
# Uses docker-compose.prod.yml
start_prod.bat
# → Environment: production
# → Database: PostgreSQL
# → Debug: False (forced)
# → CORS: Restricted
# → Security: Enabled
```

### **4. Manual Override**
```bash
# Force specific environment
set DJANGO_ENVIRONMENT=production
python manage.py runserver

# Or in Docker
environment:
  - DJANGO_ENVIRONMENT=production
```

## 📁 **Environment Files**

### **.env.dev** (Development)
```bash
DJANGO_ENVIRONMENT=development
DEBUG=True
POSTGRES_DB=openspace
POSTGRES_USER=postgres
POSTGRES_PASSWORD=12345
DB_HOST=db
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### **.env.prod** (Production)
```bash
DJANGO_ENVIRONMENT=production
DEBUG=False
POSTGRES_DB=openspace_prod
POSTGRES_USER=openspace_user
POSTGRES_PASSWORD=STRONG-PASSWORD-HERE
DB_HOST=db
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### **.env** (Local)
```bash
# Local development without Docker
DEBUG=True
SECRET_KEY=local-dev-key
# No DB_HOST = uses SQLite
```

## 🔒 **Security Features**

### **Production Automatically Enforces:**
- ✅ `DEBUG = False` (forced, ignores .env)
- ✅ PostgreSQL database (required)
- ✅ HTTPS redirects
- ✅ Secure cookies
- ✅ Security headers
- ✅ CORS restrictions
- ✅ HSTS headers
- ✅ Logging to files

### **Development Allows:**
- ✅ `DEBUG = True`
- ✅ SQLite or PostgreSQL
- ✅ Console email backend
- ✅ CORS allow all
- ✅ Relaxed security

## 🧪 **Testing Environment Detection**

```bash
# Test all scenarios
python test_environment.py

# Check current environment
python -c "from openspace.settings import ENVIRONMENT, DEBUG; print(f'Env: {ENVIRONMENT}, Debug: {DEBUG}')"

# In Docker
docker-compose -f docker-compose.dev.yml exec web python -c "from openspace.settings import ENVIRONMENT; print(ENVIRONMENT)"
```

## 🔄 **Migration Guide**

### **From Old System:**
1. ✅ Keep existing `.env.dev` and `.env.prod` files
2. ✅ Remove any hardcoded environment logic
3. ✅ Use `start_dev.bat` or `start_prod.bat`
4. ✅ Environment detection is automatic

### **No Changes Needed:**
- ✅ Docker Compose files work as before
- ✅ Environment files stay the same
- ✅ Commands remain identical
- ✅ Deployment process unchanged

## 🎯 **Best Practices**

### **Development:**
```bash
# Use Docker for consistency
start_dev.bat

# Or local for quick testing
python manage.py runserver
```

### **Production:**
```bash
# Test production locally first
start_prod.bat

# Deploy to server
docker-compose -f docker-compose.prod.yml up -d
```

### **Environment Variables:**
```bash
# Always set in Docker Compose
environment:
  - DJANGO_ENVIRONMENT=production

# Never hardcode in Dockerfile
# Never commit .env files
```

## 🚨 **Troubleshooting**

### **Wrong Environment Detected:**
```bash
# Check detection logic
python test_environment.py

# Force specific environment
set DJANGO_ENVIRONMENT=production
```

### **Settings Not Loading:**
```bash
# Check file exists
dir .env.prod

# Check Docker environment
docker-compose -f docker-compose.prod.yml exec web env | findstr DJANGO
```

### **Database Issues:**
```bash
# Check environment
python -c "from openspace.settings import DATABASES; print(DATABASES['default']['ENGINE'])"

# Should be:
# Local: sqlite3
# Development: postgresql (if DB_HOST set)
# Production: postgresql (always)
```

## ✅ **Verification Checklist**

- [ ] Local development uses SQLite
- [ ] Docker development uses PostgreSQL
- [ ] Production forces DEBUG=False
- [ ] Production enforces security settings
- [ ] Correct .env file loaded for each environment
- [ ] Environment detection works automatically
- [ ] Manual override with DJANGO_ENVIRONMENT works

Your environment management is now **production-ready** and **developer-friendly**! 🎉