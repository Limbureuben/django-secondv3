#!/usr/bin/env python3
"""
Test environment detection and configuration
"""
import os
import sys
import django
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_environment():
    """Test environment detection"""
    print("🧪 Testing Environment Detection")
    print("=" * 50)
    
    # Test different scenarios
    scenarios = [
        ("Local Development", {}),
        ("Docker Development", {"DJANGO_ENVIRONMENT": "development", "DB_HOST": "db"}),
        ("Docker Production", {"DJANGO_ENVIRONMENT": "production", "DB_HOST": "db", "DEBUG": "False"}),
    ]
    
    for scenario_name, env_vars in scenarios:
        print(f"\n📋 {scenario_name}:")
        
        # Set environment variables
        original_env = {}
        for key, value in env_vars.items():
            original_env[key] = os.environ.get(key)
            os.environ[key] = value
        
        try:
            # Import settings to trigger environment detection
            if 'openspace.settings' in sys.modules:
                del sys.modules['openspace.settings']
            
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openspace.settings')
            
            from openspace import settings
            
            print(f"  Environment: {settings.ENVIRONMENT}")
            print(f"  Debug: {settings.DEBUG}")
            print(f"  Database: {settings.DATABASES['default']['ENGINE'].split('.')[-1]}")
            print(f"  CORS: {'All origins' if settings.CORS_ALLOW_ALL_ORIGINS else 'Restricted'}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        finally:
            # Restore original environment
            for key, original_value in original_env.items():
                if original_value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = original_value

if __name__ == "__main__":
    test_environment()