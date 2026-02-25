import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcityportal.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

# Check if table exists
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='accounts_adminactivitylog';
    """)
    result = cursor.fetchall()
    
    if result:
        print("✓ Table 'accounts_adminactivitylog' EXISTS")
    else:
        print("✗ Table 'accounts_adminactivitylog' DOES NOT EXIST")
        print("\nCreating table by running migrations...")
        
        # Show current migration status
        print("\n--- Current Migration Status ---")
        call_command('showmigrations', 'accounts')
        
        print("\n--- Running Migration ---")
        call_command('migrate', 'accounts', verbosity=2)
        
        # Check again
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='accounts_adminactivitylog';
        """)
        result = cursor.fetchall()
        
        if result:
            print("\n✓ SUCCESS! Table created")
        else:
            print("\n✗ FAILED: Table still doesn't exist")
            sys.exit(1)

# Test the model
from accounts.models import AdminActivityLog
try:
    count = AdminActivityLog.objects.count()
    print(f"✓ Model accessible, log count: {count}")
    print("\n*** Migration successful! Please restart your Django server. ***")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
