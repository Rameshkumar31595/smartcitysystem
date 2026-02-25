import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcityportal.settings')
django.setup()

from accounts.models import AdminActivityLog
from django.db import connection

print("Testing AdminActivityLog table...")
print("="*60)

try:
    # Try to query the model
    count = AdminActivityLog.objects.count()
    print("✓ SUCCESS! AdminActivityLog table exists in PostgreSQL")
    print(f"  Current log count: {count}")
    
    # Check table structure
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'accounts_adminactivitylog'
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        print(f"\n  Table has {len(columns)} columns:")
        for col in columns:
            print(f"    - {col[0]}: {col[1]}")
    
    print("\n" + "="*60)
    print("✓ Everything is working! You can now:")
    print("  1. Delete issues from the admin panel")
    print("  2. View activity logs at /accounts/admin/activity-logs/")
    print("\nRestart your Django server if it's running.")
    
except Exception as e:
    print(f"✗ ERROR: {e}")
    print("\nThe table doesn't exist yet. Running migration...")
    
    from django.core.management import call_command
    try:
        call_command('migrate', 'accounts', verbosity=2)
        print("\n✓ Migration applied! Try the test again.")
    except Exception as me:
        print(f"✗ Migration error: {me}")
