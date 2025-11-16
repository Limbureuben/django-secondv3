hen # 🔐 Security Checklist for Production Deployment

## ✅ Pre-Deployment Security Tasks

### 1. **Environment Variables Security**
- [ ] Generate new `SECRET_KEY` using `python generate_keys.py`
- [ ] Generate new `FERNET_KEY` using `python generate_keys.py`
- [ ] Create strong `POSTGRES_PASSWORD` (32+ characters)
- [ ] Update `ALLOWED_HOSTS` with actual domain/IP
- [ ] Update `CORS_ALLOWED_ORIGINS` with frontend URLs
- [ ] Remove any test/development API keys
- [ ] Use production SMS API credentials

### 2. **File Security**
- [ ] Verify `.env*` files are in `.gitignore`
- [ ] Remove any hardcoded secrets from code
- [ ] Check no `.env` files are committed to git
- [ ] Ensure SSL certificates are not in git
- [ ] Remove any debug/test files

### 3. **Django Security Settings**
```python
# Verify these are set in production:
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 4. **Database Security**
- [ ] Use strong database password
- [ ] Database not exposed to internet (only internal Docker network)
- [ ] Regular database backups configured
- [ ] Database user has minimal required permissions

### 5. **Server Security**
- [ ] Server firewall configured (ports 22, 80, 443 only)
- [ ] SSH key-based authentication (disable password auth)
- [ ] Regular security updates enabled
- [ ] Non-root user for application
- [ ] Fail2ban or similar intrusion prevention

### 6. **SSL/HTTPS Security**
- [ ] SSL certificates installed
- [ ] HTTP redirects to HTTPS
- [ ] Strong SSL ciphers configured
- [ ] HSTS headers enabled

### 7. **Docker Security**
- [ ] Containers run as non-root users
- [ ] No unnecessary ports exposed
- [ ] Regular image updates
- [ ] Secrets not in Dockerfile
- [ ] Use specific image tags (not `latest`)

## 🚨 Critical Security Vulnerabilities to Avoid

### **Never Commit These Files:**
```
.env
.env.prod
.env.dev
*.key
*.pem
*.crt
backup.sql
database.dump
```

### **Never Hardcode These in Code:**
```python
# ❌ NEVER DO THIS:
SECRET_KEY = "hardcoded-secret-key"
DATABASE_PASSWORD = "mypassword123"
API_KEY = "sk-1234567890abcdef"

# ✅ ALWAYS DO THIS:
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_PASSWORD = os.getenv('POSTGRES_PASSWORD')
API_KEY = os.getenv('API_KEY')
```

### **Common Attack Vectors to Prevent:**
1. **SQL Injection**: Use Django ORM, never raw SQL with user input
2. **XSS**: Escape all user input, use Django templates
3. **CSRF**: Keep CSRF middleware enabled
4. **Clickjacking**: Set X-Frame-Options header
5. **Man-in-the-Middle**: Force HTTPS, use HSTS
6. **Brute Force**: Rate limiting, strong passwords
7. **Directory Traversal**: Validate file paths
8. **Information Disclosure**: Disable DEBUG, custom error pages

## 🛡️ Security Monitoring

### **Log Monitoring:**
```bash
# Monitor these logs for suspicious activity:
docker-compose logs nginx    # Web server access
docker-compose logs web      # Django application
docker-compose logs db       # Database queries
```

### **Security Headers Check:**
```bash
# Test security headers:
curl -I https://yourdomain.com
# Should include:
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
```

### **SSL Security Test:**
```bash
# Test SSL configuration:
openssl s_client -connect yourdomain.com:443
# Or use online tools like SSL Labs
```

## 🔄 Regular Security Maintenance

### **Weekly Tasks:**
- [ ] Check for security updates
- [ ] Review access logs for anomalies
- [ ] Verify backups are working
- [ ] Monitor resource usage

### **Monthly Tasks:**
- [ ] Update Docker images
- [ ] Review user permissions
- [ ] Test disaster recovery
- [ ] Security scan with tools

### **Quarterly Tasks:**
- [ ] Rotate API keys
- [ ] Update SSL certificates
- [ ] Security audit
- [ ] Penetration testing

## 🚀 Deployment Security Commands

### **Generate Secure Keys:**
```bash
python generate_keys.py
```

### **Security Scan Before Deployment:**
```bash
# Check for secrets in git history
git log --all --full-history -- .env*

# Scan for hardcoded secrets
grep -r "password\|secret\|key" --include="*.py" .

# Check file permissions
find . -name "*.env*" -exec ls -la {} \;
```

### **Production Deployment:**
```bash
# 1. Update environment
cp .env.prod.example .env.prod
# Edit .env.prod with secure values

# 2. Build with security
docker-compose -f docker-compose.prod.yml build --no-cache

# 3. Deploy
docker-compose -f docker-compose.prod.yml up -d

# 4. Verify security
docker-compose -f docker-compose.prod.yml exec web python manage.py check --deploy
```

## 📞 Security Incident Response

### **If Security Breach Suspected:**
1. **Immediate Actions:**
   - Take application offline
   - Change all passwords/keys
   - Review access logs
   - Document incident

2. **Investigation:**
   - Identify attack vector
   - Assess data exposure
   - Check system integrity
   - Preserve evidence

3. **Recovery:**
   - Patch vulnerabilities
   - Restore from clean backup
   - Update security measures
   - Monitor for reoccurrence

4. **Prevention:**
   - Update security procedures
   - Additional monitoring
   - Staff security training
   - Regular security audits