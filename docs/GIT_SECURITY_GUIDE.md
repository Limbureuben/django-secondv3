# 🔒 Git Security Guide - Files NOT to Push

## ❌ **NEVER PUSH THESE FILES TO GIT**

### **🔐 Environment & Secrets (CRITICAL)**
```
.env                           # Local environment file
.env.dev                       # Development environment (contains DB passwords)
.env.prod                      # Production environment (contains all secrets)
production_keys_backup.txt     # Backup of production keys
```

### **🔑 SSL Certificates & Keys**
```
nginx/ssl/                     # SSL certificate directory
*.pem                         # SSL certificates
*.key                         # Private keys
*.crt                         # Certificate files
*.p12                         # PKCS#12 files
*.pfx                         # Personal Information Exchange files
```

### **💾 Database Files & Backups**
```
db.sqlite3                    # SQLite database
*.sql                         # SQL dump files
*.dump                        # Database dump files
backup_*.sql.gz               # Compressed backups
backups/                      # Backup directory
```

### **📝 Log Files**
```
*.log                         # All log files
logs/                         # Log directory
django.log                    # Django application logs
```

### **🐍 Python Development Files**
```
__pycache__/                  # Python cache directories
*.pyc                         # Python bytecode
*.pyo                         # Python optimized bytecode
*.pyd                         # Python extension modules
venv/                         # Virtual environment
env/                          # Alternative venv name
.venv/                        # Hidden venv directory
```

### **📁 Media & Static Files**
```
media/                        # User uploaded files
staticfiles/                  # Collected static files (generated)
static_root/                  # Alternative static root
```

### **🐳 Docker Runtime Data**
```
postgres_data/                # PostgreSQL data directory
postgres_data_dev/            # Development PostgreSQL data
postgres_data_prod/           # Production PostgreSQL data
redis_data/                   # Redis data directory
```

## ✅ **SAFE TO PUSH TO GIT**

### **📋 Configuration Templates**
```
.env.example                  # Environment template (no secrets)
.env.dev.example              # Development template
.env.prod.example             # Production template
```

### **🐳 Docker Configuration**
```
docker-compose.dev.yml        # Development Docker config
docker-compose.prod.yml       # Production Docker config
Dockerfile.dev                # Development container
Dockerfile.prod               # Production container
.dockerignore                 # Docker ignore rules
```

### **🌐 Web Server Configuration**
```
nginx/nginx.conf              # Main Nginx config
nginx/conf.d/default.conf     # Server configuration
```

### **🚀 Scripts & Automation**
```
scripts/generate_keys.py      # Key generation script
scripts/setup_production.py   # Production setup script
scripts/db_access.py          # Database utilities
scripts/test_*.py             # Test scripts
*.bat                         # Windows batch scripts
*.sh                          # Shell scripts
```

### **📚 Documentation**
```
README.md                     # Main documentation
PROJECT_STRUCTURE.md          # Project structure
docs/                         # Documentation directory
deployment/                   # Deployment guides
```

### **⚙️ Project Files**
```
requirements.txt              # Python dependencies
.gitignore                    # Git ignore rules
manage.py                     # Django management
openspace/                    # Django project directory
myapp/                        # Django application
```

## 🔍 **How to Check What You're About to Push**

### **Before Committing:**
```bash
# Check what files are staged
git status

# Check what's in your working directory
git ls-files

# Check if any sensitive files are tracked
git ls-files | findstr /i "\.env"
git ls-files | findstr /i "\.key"
git ls-files | findstr /i "\.pem"
```

### **Verify .gitignore is Working:**
```bash
# These should return nothing (files ignored)
git check-ignore .env.prod
git check-ignore production_keys_backup.txt
git check-ignore db.sqlite3

# If files show up, they're NOT ignored (BAD!)
```

### **Remove Accidentally Committed Secrets:**
```bash
# If you accidentally committed secrets
git rm --cached .env.prod
git rm --cached production_keys_backup.txt
git commit -m "Remove sensitive files"

# For files already in history (DANGEROUS - rewrites history)
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch .env.prod' \
--prune-empty --tag-name-filter cat -- --all
```

## 🛡️ **Security Best Practices**

### **✅ Before Every Commit:**
1. **Check staged files:** `git status`
2. **Verify no secrets:** Look for `.env*`, `*.key`, `*.pem`
3. **Review changes:** `git diff --cached`
4. **Test .gitignore:** `git check-ignore <sensitive-file>`

### **✅ Repository Setup:**
```bash
# Always commit .gitignore first
git add .gitignore
git commit -m "Add comprehensive .gitignore"

# Then add safe files
git add README.md requirements.txt
git add docker-compose.*.yml
git add openspace/ myapp/
git commit -m "Add project files"
```

### **✅ Team Collaboration:**
```bash
# Share environment templates, not actual files
git add .env.example .env.prod.example
git commit -m "Add environment templates"

# Document required environment variables
# Never share actual values in Git
```

## 🚨 **Emergency: If Secrets Are Exposed**

### **Immediate Actions:**
1. **Change all passwords/keys immediately**
2. **Revoke API keys**
3. **Generate new SECRET_KEY and FERNET_KEY**
4. **Update production environment**
5. **Remove from Git history**

### **Prevention:**
```bash
# Use git hooks to prevent commits with secrets
# Create .git/hooks/pre-commit:
#!/bin/bash
if git diff --cached --name-only | grep -E "\.(env|key|pem)$"; then
    echo "❌ Attempting to commit sensitive files!"
    exit 1
fi
```

## 📋 **Quick Security Checklist**

- [ ] `.env*` files are in `.gitignore`
- [ ] No passwords in code or config files
- [ ] SSL certificates not committed
- [ ] Database files ignored
- [ ] Log files ignored
- [ ] Virtual environment ignored
- [ ] Only templates (`.example`) committed
- [ ] Secrets stored securely outside Git
- [ ] Team uses environment templates
- [ ] Production keys generated separately

## 🎯 **Summary: Safe Git Workflow**

```bash
# 1. Setup .gitignore first
git add .gitignore
git commit -m "Add security .gitignore"

# 2. Add only safe files
git add README.md requirements.txt
git add docker-compose.*.yml Dockerfile.*
git add openspace/ myapp/ nginx/
git add scripts/ docs/ deployment/
git add *.example

# 3. Never add these patterns
# .env* (except .example)
# *.key, *.pem, *.crt
# *.sql, *.dump, backup_*
# *.log, logs/
# venv/, __pycache__/

# 4. Verify before pushing
git status
git ls-files | grep -E "\.(env|key|pem|sql|log)$"
```

Your `.gitignore` is already configured correctly to prevent these security issues! 🛡️