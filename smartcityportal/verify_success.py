import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcityportal.settings')
django.setup()

from accounts.models import AdminActivityLog

try:
    count = AdminActivityLog.objects.count()
    print("SUCCESS! AdminActivityLog table exists in PostgreSQL")
    print(f"Current log count: {count}")
    print("\nYou can now:")
    print("1. Delete issues from admin panel")
    print("2. View logs at http://127.0.0.1:8000/accounts/admin/activity-logs/")
    print("\nPlease restart your Django development server!")
except Exception as e:
    print(f"ERROR: {e}")
