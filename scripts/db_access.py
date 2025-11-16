#!/usr/bin/env python3
"""
Database Access Script for Production
Provides secure access to production database
"""

import os
import sys
import subprocess
from pathlib import Path

def get_db_credentials():
    """Get database credentials from .env.prod"""
    env_file = Path('../.env.prod')
    if not env_file.exists():
        print(" .env.prod file not found!")
        return None
    
    credentials = {}
    with open(env_file, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                credentials[key] = value
    
    return {
        'database': credentials.get('POSTGRES_DB', 'openspace_prod'),
        'user': credentials.get('POSTGRES_USER', 'openspace_user'),
        'password': credentials.get('POSTGRES_PASSWORD', ''),
        'host': credentials.get('DB_HOST', 'db'),
        'port': credentials.get('DB_PORT', '5432')
    }

def access_production_db():
    """Access production database"""
    print(" Production Database Access")
    print("=" * 40)
    
    creds = get_db_credentials()
    if not creds:
        return False
    
    print(f"Database: {creds['database']}")
    print(f"User: {creds['user']}")
    
    # Docker access command
    print("\n Docker Access:")
    print("docker-compose -f docker-compose.prod.yml exec db psql -U openspace_user openspace_prod")
    
    # Manual access info
    print(f"\n Manual Access:")
    print(f"Host: {creds['host']}")
    print(f"Port: {creds['port']}")
    print(f"Database: {creds['database']}")
    print(f"Username: {creds['user']}")
    print(f"Password: {creds['password']}")

if __name__ == "__main__":
    access_production_db()