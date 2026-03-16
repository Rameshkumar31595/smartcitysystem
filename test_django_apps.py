#!/usr/bin/env python
"""
Test Django app imports to ensure no circular dependencies or syntax errors.
"""
import os
import sys
import django
from pathlib import Path

# Setup path exactly like Vercel would
repo_root = Path(__file__).resolve().parent
django_root = repo_root / "smartcityportal"
sys.path.insert(0, str(django_root))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartcityportal.settings")

print("Setting up Django...")
try:
    django.setup()
    print("✓ Django setup successful")
except Exception as e:
    print(f"✗ Django setup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("Testing Django apps import...")

# Test each installed app
apps_to_test = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'services', 
    'issues',
]

for app_name in apps_to_test:
    try:
        if app_name.startswith('django.'):
            __import__(app_name)
        else:
            from django.apps import apps
            apps.get_app_config(app_name)
        print(f"✓ {app_name}")
    except Exception as e:
        print(f"✗ {app_name}: {e}")

print()
print("Testing models import...")

try:
    from accounts.models import User
    print("✓ accounts.models.User imported successfully")
except Exception as e:
    print(f"✗ accounts.models.User: {e}")

try:
    from services.models import Service
    print("✓ services.models.Service imported successfully")
except Exception as e:
    print(f"✗ services.models.Service: {e}")

try:
    from issues.models import Issue
    print("✓ issues.models.Issue imported successfully")
except Exception as e:
    print(f"✗ issues.models.Issue: {e}")

print()
print("Testing URL routing...")

try:
    from django.urls import get_resolver
    resolver = get_resolver()
    print(f"✓ URL resolver loaded successfully")
    print(f"  Total URL patterns: {len(resolver.url_patterns)}")
except Exception as e:
    print(f"✗ URL resolver failed: {e}")
    import traceback
    traceback.print_exc()

print()
print("Testing static files...")

try:
    from django.conf import settings
    print(f"✓ Settings loaded")
    print(f"  STATIC_URL: {settings.STATIC_URL}")
    print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"  STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
except Exception as e:
    print(f"✗ Static settings error: {e}")

print()
print("✓ All Django components tested successfully")
