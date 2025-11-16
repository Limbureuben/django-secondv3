# 🚀 Step-by-Step Deployment Guide

## 📋 Prerequisites

### **Local Machine Requirements:**
- Docker Desktop installed
- Git configured
- Python 3.11+ installed

### **University Server Requirements:**
- Ubuntu 20.04+ or CentOS 7+
- 2GB+ RAM (4GB recommended)
- 20GB+ disk space
- Root or sudo access
- Internet connection

## 🧪 **STEP 1: Test Locally First**

### **1.1 Generate Secure Keys**
```bash
# Generate production keys
python generate_keys.py

# Copy output to .env.prod file
```

### **1.2 Test Development Environment**
```bash
# Test development setup
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up -d

# Check if running
docker-compose -f docker-compose.dev.yml ps

# Test endpoints
curl http://localhost:8000
curl http://localhost:8000/admin/

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop when done
docker-compose -f docker-compose.dev.yml down
```

### **1.3 Test Production Environment**
```bash
# Update .env.prod with secure values
cp .env.prod.example .env.prod
# Edit .env.prod with generated keys

# Test production setup
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Check if running
docker-compose -f docker-compose.prod.yml ps

# Test endpoints
curl http://localhost
curl http://localhost/admin/

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop when done
docker-compose -f docker-compose.prod.yml down
```

### **1.4 Automated Testing**
```bash
# Run comprehensive tests
python test_environments.py
```

## 🏗️ **STEP 2: Prepare for University Server**

### **2.1 Security Checklist**
```bash
# Run security checklist
cat SECURITY_CHECKLIST.md

# Verify no secrets in git
git log --all --full-history -- .env*
grep -r "password\|secret\|key" --include="*.py" .
```

### **2.2 Update Configuration**
```bash
# Update .env.prod with university server details
ALLOWED_HOSTS=university-server-ip,yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# Update nginx configuration
# Edit nginx/conf.d/default.conf
server_name university-server-ip yourdomain.com;
```

### **2.3 Commit Changes**
```bash
# Add changes (but NOT .env files)
git add .
git commit -m "Prepare for production deployment"
git push origin main
```

## 🚢 **STEP 3: Transfer to University Server**

### **Option A: Git Clone (Recommended)**
```bash
# On university server
ssh user@university-server
cd /opt
sudo git clone https://github.com/yourusername/openspace.git
cd openspace
sudo chown -R $USER:$USER .
```

### **Option B: SCP Upload**
```bash
# On local machine
tar --exclude='.git' --exclude='node_modules' --exclude='__pycache__' -czf openspace.tar.gz .
scp openspace.tar.gz user@university-server:/tmp/

# On university server
cd /opt
sudo tar -xzf /tmp/openspace.tar.gz
sudo mv openspace-* openspace
cd openspace
sudo chown -R $USER:$USER .
```

## 🐳 **STEP 4: Install Docker on University Server**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again for group changes
exit
ssh user@university-server
```

## ⚙️ **STEP 5: Configure Production Environment**

```bash
cd /opt/openspace

# Make scripts executable
chmod +x setup.sh entrypoint.prod.sh entrypoint.dev.sh generate_keys.py

# Run setup script
./setup.sh

# Create production environment file
cp .env.prod.example .env.prod

# Generate secure keys
python3 generate_keys.py

# Edit .env.prod with secure values
nano .env.prod
# Update: SECRET_KEY, POSTGRES_PASSWORD, FERNET_KEY, ALLOWED_HOSTS, domain names
```

## 🚀 **STEP 6: Deploy Application**

```bash
# Build production containers
docker-compose -f docker-compose.prod.yml build

# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Check container status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Test deployment
curl http://university-server-ip
curl http://university-server-ip/admin/
```

## 🔒 **STEP 7: Configure Security**

### **7.1 Firewall Setup**
```bash
# Configure UFW firewall
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS (if using SSL)
sudo ufw enable

# Check firewall status
sudo ufw status
```

### **7.2 SSL Setup (Optional but Recommended)**
```bash
# Install Certbot
sudo apt install certbot

# Get SSL certificate (replace with your domain)
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates to nginx
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem
sudo chown $USER:$USER nginx/ssl/*.pem

# Uncomment SSL lines in nginx/conf.d/default.conf
nano nginx/conf.d/default.conf

# Restart nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

### **7.3 Auto-start Service**
```bash
# Create systemd service
sudo nano /etc/systemd/system/openspace.service
```

Add this content:
```ini
[Unit]
Description=OpenSpace Docker Compose
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/openspace
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable openspace.service
sudo systemctl start openspace.service

# Check service status
sudo systemctl status openspace.service
```

## 📊 **STEP 8: Verify Deployment**

### **8.1 Health Checks**
```bash
# Check all containers are running
docker-compose -f docker-compose.prod.yml ps

# Check application health
curl -f http://university-server-ip/health/ || echo "Health check failed"

# Check database connection
docker-compose -f docker-compose.prod.yml exec web python manage.py check --database default

# Check static files
curl -f http://university-server-ip/static/admin/css/base.css || echo "Static files not served"
```

### **8.2 Security Verification**
```bash
# Check security headers
curl -I http://university-server-ip

# Run Django security check
docker-compose -f docker-compose.prod.yml exec web python manage.py check --deploy

# Verify no debug mode
docker-compose -f docker-compose.prod.yml exec web python -c "from django.conf import settings; print('DEBUG:', settings.DEBUG)"
```

### **8.3 Performance Test**
```bash
# Simple load test
for i in {1..10}; do curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" http://university-server-ip; done
```

## 🔄 **STEP 9: Setup Monitoring & Backups**

### **9.1 Database Backups**
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups/openspace"
mkdir -p $BACKUP_DIR
cd /opt/openspace
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U openspace_user openspace_prod | gzip > $BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql.gz
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete
EOF

chmod +x backup.sh

# Add to crontab for daily backups
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/openspace/backup.sh") | crontab -
```

### **9.2 Log Rotation**
```bash
# Setup log rotation
sudo nano /etc/logrotate.d/openspace
```

Add:
```
/opt/openspace/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 644 root root
}
```

## 🎉 **STEP 10: Access Your Application**

### **Application URLs:**
- **Main Application**: `http://university-server-ip`
- **Admin Panel**: `http://university-server-ip/admin`
- **API Documentation**: `http://university-server-ip/api/docs/`
- **GraphQL**: `http://university-server-ip/graphql`
- **Celery Monitoring**: `http://university-server-ip/flower`

### **Default Admin Credentials:**
- Username: (created during deployment)
- Password: (set during deployment)

## 🆘 **Troubleshooting**

### **Common Issues:**
```bash
# Container won't start
docker-compose -f docker-compose.prod.yml logs web

# Database connection issues
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell

# Static files not loading
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Permission issues
sudo chown -R $USER:$USER /opt/openspace

# Port already in use
sudo lsof -i :80
sudo kill -9 <PID>

# Clean restart
docker-compose -f docker-compose.prod.yml down
docker system prune -f
docker-compose -f docker-compose.prod.yml up -d
```

### **Get Help:**
```bash
# View all logs
docker-compose -f docker-compose.prod.yml logs

# Access container shell
docker-compose -f docker-compose.prod.yml exec web bash

# Check Django configuration
docker-compose -f docker-compose.prod.yml exec web python manage.py diffsettings
```

## ✅ **Deployment Complete!**

Your OpenSpace application is now running securely on the university server with:
- ✅ Production-grade security
- ✅ Automated backups
- ✅ SSL encryption (if configured)
- ✅ Auto-restart on reboot
- ✅ Monitoring and logging
- ✅ Scalable architecture