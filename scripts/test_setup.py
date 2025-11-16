#!/usr/bin/env python3
"""
Quick Setup Test Script for OpenSpace Django Application
Tests basic functionality without Docker
"""

import os
import sys
import subprocess
import django
from pathlib import Path

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_python_setup():
    """Test Python and virtual environment"""
    print("🐍 Testing Python Setup...")
    
    # Check Python version
    print(f"  Python version: {sys.version}")
    
    # Check if in virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"  Virtual environment: {'✅ Active' if in_venv else '⚠️ Not active'}")
    
    # Check required packages
    required_packages = ['django', 'psycopg2', 'redis', 'celery', 'graphene_django']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}: Installed")
        except ImportError:
            print(f"  ❌ {package}: Missing")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def test_django_setup():
    """Test Django configuration"""
    print("\n🎯 Testing Django Setup...")
    
    try:
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openspace.settings')
        django.setup()
        
        from django.conf import settings
        from django.core.management import execute_from_command_line
        
        print(f"  ✅ Django settings loaded")
        print(f"  Debug mode: {settings.DEBUG}")
        print(f"  Database engine: {settings.DATABASES['default']['ENGINE']}")
        
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("  ✅ Database connection: OK")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Django setup failed: {e}")
        return False

def test_environment_files():
    """Test environment configuration"""
    print("\n📄 Testing Environment Files...")
    
    files_to_check = [
        ('.env', 'Development environment'),
        ('.env.example', 'Environment template'),
        ('requirements.txt', 'Python dependencies'),
        ('docker-compose.dev.yml', 'Development Docker config'),
        ('docker-compose.prod.yml', 'Production Docker config'),
    ]
    
    all_exist = True
    for filename, description in files_to_check:
        if os.path.exists(filename):
            print(f"  ✅ {filename}: {description}")
        else:
            print(f"  ❌ {filename}: Missing - {description}")
            all_exist = False
    
    return all_exist

def test_docker_setup():
    """Test Docker availability"""
    print("\n🐳 Testing Docker Setup...")
    
    # Check Docker
    docker_ok, stdout, stderr = run_command("docker --version")
    if docker_ok:
        print(f"  ✅ Docker: {stdout.strip()}")
    else:
        print(f"  ❌ Docker: Not available")
        return False
    
    # Check Docker Compose
    compose_ok, stdout, stderr = run_command("docker-compose --version")
    if compose_ok:
        print(f"  ✅ Docker Compose: {stdout.strip()}")
    else:
        print(f"  ❌ Docker Compose: Not available")
        return False
    
    return True

def test_basic_django_commands():
    """Test basic Django management commands"""
    print("\n⚙️ Testing Django Commands...")
    
    commands = [
        ("python manage.py check", "Django configuration check"),
        ("python manage.py migrate --dry-run", "Database migrations (dry run)"),
        ("python manage.py collectstatic --dry-run --noinput", "Static files collection (dry run)"),
    ]
    
    all_passed = True
    for command, description in commands:
        success, stdout, stderr = run_command(command)
        if success:
            print(f"  ✅ {description}: OK")
        else:
            print(f"  ❌ {description}: Failed")
            print(f"      Error: {stderr.strip()}")
            all_passed = False
    
    return all_passed

def main():
    """Run all tests"""
    print("🧪 OpenSpace Django Project Setup Test")
    print("=" * 50)
    
    tests = [
        ("Python Setup", test_python_setup),
        ("Environment Files", test_environment_files),
        ("Docker Setup", test_docker_setup),
        ("Django Setup", test_django_setup),
        ("Django Commands", test_basic_django_commands),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\n🚀 Next steps:")
        print("  1. Run: python manage.py migrate")
        print("  2. Run: python manage.py createsuperuser")
        print("  3. Run: python manage.py runserver")
        print("  4. Or use Docker: start_dev.bat")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please fix the issues above.")
        print("\n💡 Common solutions:")
        print("  - Install missing packages: pip install -r requirements.txt")
        print("  - Create .env file: copy .env.example .env")
        print("  - Install Docker Desktop")
        print("  - Activate virtual environment: venv\\Scripts\\activate")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)