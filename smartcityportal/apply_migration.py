import subprocess
import sys

print("="*60)
print("CHECKING MIGRATION STATUS")
print("="*60)

# Run showmigrations
result = subprocess.run(
    [sys.executable, 'manage.py', 'showmigrations', 'accounts'],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

print("\n" + "="*60)
print("APPLYING MIGRATION")
print("="*60)

# Run migrate
result = subprocess.run(
    [sys.executable, 'manage.py', 'migrate', 'accounts'],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

print("\n" + "="*60)
print("VERIFYING TABLE EXISTS")
print("="*60)

# Test the model
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcityportal.settings')
django.setup()

from accounts.models import AdminActivityLog
try:
    count = AdminActivityLog.objects.count()
    print(f"✓ SUCCESS! AdminActivityLog table exists")
    print(f"  Current log count: {count}")
    print("\n*** MIGRATION COMPLETE! Restart your Django server. ***")
except Exception as e:
    print(f"✗ ERROR: {e}")
    print("\nThe table still doesn't exist. Creating it manually...")
    
    from django.db import connection
    with connection.cursor() as cursor:
        # Create table manually if migration didn't work
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts_adminactivitylog (
                id SERIAL PRIMARY KEY,
                admin_id INTEGER REFERENCES accounts_user(id) ON DELETE SET NULL,
                action_type VARCHAR(20) NOT NULL,
                description TEXT NOT NULL,
                target_model VARCHAR(50),
                target_id INTEGER,
                target_info TEXT,
                ip_address INET,
                timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS accounts_adminactivitylog_admin_id ON accounts_adminactivitylog(admin_id);
            CREATE INDEX IF NOT EXISTS accounts_adminactivitylog_timestamp ON accounts_adminactivitylog(timestamp DESC);
        """)
        print("✓ Table created manually!")
