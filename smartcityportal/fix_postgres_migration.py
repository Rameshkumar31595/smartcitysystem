import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcityportal.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

print("Database Engine:", connection.settings_dict['ENGINE'])
print("Database Name:", connection.settings_dict['NAME'])
print("\n" + "="*60)

# Check if table exists in PostgreSQL
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'accounts_adminactivitylog';
    """)
    result = cursor.fetchall()
    
    if result:
        print("✓ Table 'accounts_adminactivitylog' EXISTS in PostgreSQL")
    else:
        print("✗ Table 'accounts_adminactivitylog' DOES NOT EXIST in PostgreSQL")
        print("\n--- Checking Migration Status ---")
        call_command('showmigrations', 'accounts')
        
        print("\n--- Applying Migration ---")
        try:
            call_command('migrate', 'accounts', verbosity=2)
            print("\n✓ Migration applied successfully!")
        except Exception as e:
            print(f"\n✗ Error applying migration: {e}")

# Test the model
from accounts.models import AdminActivityLog
try:
    count = AdminActivityLog.objects.count()
    print(f"\n✓ Model is accessible! Current log count: {count}")
    print("\n*** SUCCESS! Please restart your Django server. ***")
except Exception as e:
    print(f"\n✗ Error accessing model: {e}")
