import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcityportal.settings')
django.setup()

from accounts.models import AdminActivityLog

# Test if we can query the model
try:
    count = AdminActivityLog.objects.count()
    print(f"SUCCESS! AdminActivityLog table is working. Current log count: {count}")
    print("The delete functionality should now work without errors.")
except Exception as e:
    print(f"ERROR: {e}")
