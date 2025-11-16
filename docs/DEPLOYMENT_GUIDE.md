# 🚀 University Server Deployment Guide

## 📋 Pre-Deployment Checklist

### 1. Update `.env.prod` File

```bash
# Replace these values:
ALLOWED_HOSTS=your-university-domain.edu,www.your-university-domain.edu,SERVER_IP_ADDRESS
SECRET_KEY=<generate-new-secret-key>
POSTGRES_PASSWORD=<strong-password>
FERNET_KEY=<generate-new-fernet-key>
```

### 2. Generate Secure Keys

```bash
# Generate SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Generate FERNET_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 3. Update Nginx Configuration

Edit `nginx/conf.d/default.conf`:
```nginx
server_name your-university-domain.edu www.your-university-domain.edu;
```

---

## 🏫 On University Server

### Step 1: Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### Step 2: Transfer Project

**Option A: Using Git**
```bash
cd /opt
sudo git clone https://github.com/yourusername/openspace.git
cd openspace
```

**Option B: Using SCP**
```bash
# On your local machine
tar -czf openspace.tar.gz django-secondv3/
scp openspace.tar.gz user@university-server:/opt/

# On server
cd /opt
tar -xzf openspace.tar.gz
cd django-secondv3
```

### Step 3: Setup SSL Certificates

**Option A: Let's Encrypt (Recommended)**
```bash
sudo apt-get update
sudo apt-get install certbot

# Get certificate
sudo certbot certonly --standalone -d your-university-domain.edu

# Copy to project
sudo cp /etc/letsencrypt/live/your-university-domain.edu/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-university-domain.edu/privkey.pem nginx/ssl/key.pem
sudo chown $USER:$USER nginx/ssl/*.pem
```

**Option B: University Provided Certificates**
```bash
# Copy your university's SSL certificates
cp /path/to/certificate.crt nginx/ssl/cert.pem
cp /path/to/private.key nginx/ssl/key.pem
```

### Step 4: Update Production Settings

```bash
# Edit .env.prod with university details
nano .env.prod

# Update these:
ALLOWED_HOSTS=your-university-domain.edu,www.your-university-domain.edu,SERVER_IP
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Step 5: Deploy

```bash
# Make scripts executable
chmod +x *.sh *.bat

# Build and start
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Step 6: Setup Firewall

```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### Step 7: Auto-start on Boot

```bash
sudo nano /etc/systemd/system/openspace.service
```

Add:
```ini
[Unit]
Description=OpenSpace Docker Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/django-secondv3
ExecStart=/usr/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable openspace.service
sudo systemctl start openspace.service
```

---

## 🔒 SSL Certificate Setup

### Current Status
- `nginx/ssl/cert.pem` - Self-signed certificate (for testing only)
- `nginx/ssl/key.pem` - Self-signed key (for testing only)

### For Production
**Delete test certificates and use real ones:**

```bash
# Remove test certificates
rm nginx/ssl/cert.pem nginx/ssl/key.pem

# Add real certificates (choose one method above)
```

---

## 📊 Post-Deployment

### Access Your Application
- Main App: `https://your-university-domain.edu`
- Admin Panel: `https://your-university-domain.edu/admin`
- GraphQL: `https://your-university-domain.edu/graphql`

### Useful Commands

```bash
# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart services
docker-compose -f docker-compose.prod.yml restart

# Stop everything
docker-compose -f docker-compose.prod.yml down

# Database backup
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U openspace_user openspace_prod > backup.sql

# Update application
git pull origin main
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

---

## 🔧 Troubleshooting

### Check Container Status
```bash
docker-compose -f docker-compose.prod.yml ps
```

### View Specific Logs
```bash
docker logs openspace_web_prod
docker logs openspace_db_prod
docker logs openspace_nginx_prod
```

### Restart Specific Service
```bash
docker-compose -f docker-compose.prod.yml restart web
```

### Clean Restart
```bash
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📝 Important Notes

1. **SSL Certificates**: Replace self-signed certificates with real ones before going live
2. **Passwords**: Change all default passwords in `.env.prod`
3. **Backups**: Setup automated daily database backups
4. **Monitoring**: Monitor logs regularly for errors
5. **Updates**: Keep Docker images and dependencies updated

---

## ✅ Deployment Checklist

- [ ] Updated `.env.prod` with university domain
- [ ] Generated new SECRET_KEY and FERNET_KEY
- [ ] Changed database password
- [ ] Obtained real SSL certificates
- [ ] Updated nginx configuration with domain
- [ ] Tested on university server
- [ ] Created superuser account
- [ ] Setup firewall rules
- [ ] Configured auto-start service
- [ ] Setup backup automation
- [ ] Documented admin credentials (securely)
