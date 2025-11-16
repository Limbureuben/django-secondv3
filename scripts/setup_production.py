#!/usr/bin/env python3
"""
Production Environment Setup Script
Generates secure keys and creates .env.prod file
"""

import os
import secrets
import string
from cryptography.fernet import Fernet
from pathlib import Path

def generate_django_secret_key():
    """Generate Django SECRET_KEY"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(50))

def generate_fernet_key():
    """Generate Fernet encryption key"""
    return Fernet.generate_key().decode()

def generate_strong_password():
    """Generate strong database password"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(secrets.choice(chars) for _ in range(32))

def create_production_env():
    """Create .env.prod with secure keys"""
    
    print("🔐 Production Environment Setup")
    print("=" * 50)
    
    # Generate secure keys
    secret_key = generate_django_secret_key()
    fernet_key = generate_fernet_key()
    db_password = generate_strong_password()
    
    print("✅ Generated secure keys")
    
    # Get user input for deployment details
    print("\n📋 Enter deployment details:")
    domain = input("Domain (e.g., yourdomain.com): ").strip() or "yourdomain.com"
    server_ip = input("Server IP (e.g., 192.168.1.100): ").strip() or "192.168.1.100"
    
    # Email settings
    print("\n📧 Email Configuration:")
    email_user = input("Email (e.g., your-email@gmail.com): ").strip() or "your-email@gmail.com"
    email_password = input("Email App Password: ").strip() or "your-app-password"
    
    # SMS settings (optional)
    print("\n📱 SMS Configuration (optional, press Enter to skip):")
    at_username = input("Africa's Talking Username: ").strip() or "production_username"
    at_api_key = input("Africa's Talking API Key: ").strip() or "your-production-at-api-key"
    
    # Create .env.prod content
    env_content = f"""# ========================================
# PRODUCTION ENVIRONMENT - AUTO GENERATED
# ========================================
# Generated on: {os.popen('date /t').read().strip()} {os.popen('time /t').read().strip()}

# ========================================
# DJANGO CORE SETTINGS
# ========================================
DJANGO_ENVIRONMENT=production
SECRET_KEY={secret_key}
DEBUG=False
ALLOWED_HOSTS={domain},www.{domain},{server_ip}

# ========================================
# DATABASE CONFIGURATION
# ========================================
POSTGRES_DB=openspace_prod
POSTGRES_USER=openspace_user
POSTGRES_PASSWORD={db_password}
DB_HOST=db
DB_PORT=5432

# ========================================
# REDIS CONFIGURATION
# ========================================
REDIS_URL=redis://redis:6379/0

# ========================================
# CELERY CONFIGURATION
# ========================================
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# ========================================
# EMAIL CONFIGURATION
# ========================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER={email_user}
EMAIL_HOST_PASSWORD={email_password}
DEFAULT_FROM_EMAIL={email_user}

# ========================================
# FRONTEND & BACKEND URLS
# ========================================
FRONTEND_URL=https://{domain}
BACKEND_URL=https://api.{domain}

# ========================================
# SMS SERVICES
# ========================================
AT_USERNAME={at_username}
AT_API_KEY={at_api_key}

BEEM_API_KEY=76dae10b6f9e7fd7
BEEM_SECRET_KEY=MDc5MzM3YzhkMDE2YzA1YjYxYjc1M2M5Njc1MGQzYzQ4Mzk0ZTc0MWU2Yjk5NzA4ZWI2YTA1OTY4MTNlNWM4Mg==
BEEM_SENDER_ID=OPENSPACE

# ========================================
# ENCRYPTION
# ========================================
FERNET_KEY={fernet_key}

# ========================================
# CORS SETTINGS
# ========================================
CORS_ALLOWED_ORIGINS=https://{domain},https://www.{domain}

# ========================================
# SECURITY SETTINGS
# ========================================
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS=DENY
"""

    # Write .env.prod file
    env_file = Path('../.env.prod')
    env_file.write_text(env_content, encoding='utf-8')
    
    print(f"\n✅ Created {env_file.absolute()}")
    
    # Create backup of keys
    keys_backup = f"""
# BACKUP YOUR PRODUCTION KEYS
# Save this information securely!

SECRET_KEY={secret_key}
POSTGRES_PASSWORD={db_password}
FERNET_KEY={fernet_key}

Domain: {domain}
Server IP: {server_ip}
Email: {email_user}
"""
    
    backup_file = Path('../production_keys_backup.txt')
    backup_file.write_text(keys_backup, encoding='utf-8')
    
    print(f"✅ Created backup: {backup_file.absolute()}")
    
    # Security warnings
    print("\n🚨 SECURITY WARNINGS:")
    print("=" * 50)
    print("1. ✅ .env.prod created with secure keys")
    print("2. ⚠️  NEVER commit .env.prod to git")
    print("3. 🔒 Store production_keys_backup.txt securely")
    print("4. 🔄 Update email password with app-specific password")
    print("5. 📱 Update SMS API keys with production credentials")
    print("6. 🌐 Update domain and server IP before deployment")
    
    print(f"\n🚀 Next steps:")
    print("1. Review and edit .env.prod if needed")
    print("2. Test production: start_prod.bat")
    print("3. Deploy to server")
    
    return True

if __name__ == "__main__":
    try:
        create_production_env()
        input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n⏹️ Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Press Enter to exit...")