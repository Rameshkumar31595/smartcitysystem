import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcityportal.settings')
django.setup()

from accounts.models import AdminActivityLog
from django.db import connection

# Check if table exists
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='accounts_adminactivitylog';
    """)
    result = cursor.fetchall()
    if result:
        print("✓ AdminActivityLog table EXISTS in database")
        print(f"  Table name: {result[0][0]}")
    else:
        print("✗ AdminActivityLog table DOES NOT EXIST")
        print("\nAttempting to create table...")
        from django.core.management import call_command
        call_command('migrate', 'accounts', '--verbosity', '2')

# Test model
try:
    count = AdminActivityLog.objects.count()
    print(f"✓ Model is accessible, current log count: {count}")
except Exception as e:
    print(f"✗ Error accessing model: {e}")
