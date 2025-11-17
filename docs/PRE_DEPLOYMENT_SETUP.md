# 📦 Pre-Deployment Setup (Do This NOW Before Going to University)

## ✅ What You Need from University IT Department

1. **Server Access**
   - SSH username and password
   - Server IP address
   - Domain name (e.g., openspace.university.ac.tz)

2. **SSL Certificate** (Ask IT department)
   - Certificate file (.crt or .pem)
   - Private key file (.key or .pem)
   - OR they can help you get Let's Encrypt certificate

3. **Firewall Ports** (Ask them to open)
   - Port 80 (HTTP)
   - Port 443 (HTTPS)
   - Port 22 (SSH - should already be open)

---

## 🔧 Setup NOW (Before University)

### 1. Update `.env.prod` with University Details

Ask university for:
- Domain name
- Server IP address

Then update:

```bash
ALLOWED_HOSTS=openspace.university.ac.tz,SERVER_IP_ADDRESS,localhost
```

### 2. Generate Production Keys

Run this command NOW and save the output by  copy and paste them keys in .env.prod:

```bash
cd scripts
python generate_keys.py
 
 

```

Update `.env.prod`:
```bash
SECRET_KEY=<paste-generated-secret-key>
FERNET_KEY=<paste-generated-fernet-key>
POSTGRES_PASSWORD=<create-strong-password>
```

### 3. Update Nginx Config

Edit `nginx/conf.d/default.conf`:

Replace:
```nginx
server_name localhost;
```

With:
```nginx
server_name openspace.university.ac.tz;
```

### 4. Enable Production Security

In `.env.prod`, change:
```bash
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 5. Push to GitHub

```bash
# Add .gitignore to protect secrets
git add .
git commit -m "Production ready configuration"
git push origin main
```

---

## 📦 What to Bring to University

### Option 1: USB Drive (Recommended)
```bash
# Create deployment package
tar -czf openspace-deployment.tar.gz django-secondv3/
# Copy to USB drive
```

### Option 2: GitHub (If university has internet)
- Just need your GitHub repository URL
- Clone directly on server

---

##  At University Server (Quick Deploy)

### Step 1: Transfer Files (5 minutes)

**If using USB:**
```bash
# Copy from USB to server
scp openspace-deployment.tar.gz user@SERVER_IP:/home/user/
ssh user@SERVER_IP
tar -xzf openspace-deployment.tar.gz
cd django-secondv3
```

**If using GitHub:**
```bash
ssh user@SERVER_IP
git clone https://github.com/yourusername/openspace.git
cd openspace
```

### Step 2: Install Docker (5 minutes)

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Logout and login again
```

### Step 3: Setup SSL Certificates (10 minutes)

**Option A: University Provided Certificates**
```bash
# Copy certificates from IT department
cp /path/from/IT/certificate.crt nginx/ssl/cert.pem
cp /path/from/IT/private.key nginx/ssl/key.pem
```

**Option B: Let's Encrypt (if allowed)**
```bash
sudo apt-get install certbot
sudo certbot certonly --standalone -d openspace.university.ac.tz
sudo cp /etc/letsencrypt/live/openspace.university.ac.tz/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/openspace.university.ac.tz/privkey.pem nginx/ssl/key.pem
sudo chown $USER:$USER nginx/ssl/*.pem
```

### Step 4: Deploy (5 minutes)

```bash
# Build and start But generaly this all are running in  just make the scripts executable .sh and .bat then running 
start_prod.bat
```

### Step 5: Test

Open browser: `https://openspace.university.ac.tz/admin`

---

## 🚨 Quick Troubleshooting

### If containers won't start:
```bash
docker-compose --env-file .env.prod -f docker-compose.prod.yml logs
```

### If can't access website:
```bash
# Check firewall
sudo ufw status
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### If database errors:
```bash
# Reset database
docker-compose --env-file .env.prod -f docker-compose.prod.yml down -v
docker-compose --env-file .env.prod -f docker-compose.prod.yml up -d
```

---

## 📋 Deployment Checklist (Print This!)

**BEFORE Going to University:**
- [ ] Update `.env.prod` with university domain
- [ ] Generate new SECRET_KEY
- [ ] Generate new FERNET_KEY  
- [ ] Change POSTGRES_PASSWORD
- [ ] Update nginx config with domain
- [ ] Enable SSL security settings
- [ ] Push to GitHub OR copied to USB


**AT University (Ask IT Department):**
- [ ] Server IP address: _______________
- [ ] Domain name: _______________
- [ ] SSH username: _______________
- [ ] SSH password: _______________
- [ ] SSL certificate location: _______________
- [ ] Ports 80, 443 opened? Yes/No

**Deployment Steps:**
- [ ] Transferr iles to server
- [ ] Installed Docker
- [ ] Copied SSL certificates to nginx/ssl/
- [ ] Built Docker images
- [ ] Started containers
- [ ] Created superuser
- [ ] Tested website access
- [ ] Setup auto-start service


