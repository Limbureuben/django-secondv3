#!/usr/bin/env python3
"""
Quick Key Generator for OpenSpace Django Application
Generates individual keys for manual copying
"""

import secrets
import string
from cryptography.fernet import Fernet

def generate_django_secret_key():
    """Generate a secure Django SECRET_KEY"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(50))

def generate_fernet_key():
    """Generate a secure Fernet encryption key"""
    return Fernet.generate_key().decode()

def generate_strong_password():
    """Generate a strong database password"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(secrets.choice(chars) for _ in range(32))

def main():
    print("🔐 Quick Key Generator")
    print("=" * 30)
    
    print("\n📋 Individual Keys:")
    print("-" * 30)
    
    print(f"SECRET_KEY={generate_django_secret_key()}")
    print(f"POSTGRES_PASSWORD={generate_strong_password()}")
    print(f"FERNET_KEY={generate_fernet_key()}")
    
    print("\n💡 For complete setup, use: setup_prod.bat")

if __name__ == "__main__":
    main()