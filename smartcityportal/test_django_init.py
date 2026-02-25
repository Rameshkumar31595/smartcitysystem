"""
Test script to verify Django initialization
Run this to check if Django can start properly with production settings
"""
import os
import sys

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcityportal.settings')

try:
    import django
    print("✓ Django imported successfully")
    
    django.setup()
    print("✓ Django setup completed")
    
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("✓ WSGI application created")
    
    from django.conf import settings
    print(f"✓ DEBUG={settings.DEBUG}")
    print(f"✓ ALLOWED_HOSTS={settings.ALLOWED_HOSTS}")
    print(f"✓ DATABASE={settings.DATABASES['default']['ENGINE']}")
    
    # Test database connection
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✓ Database connection successful: {result}")
    
    print("\n✅ All checks passed! Django is configured correctly.")
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
