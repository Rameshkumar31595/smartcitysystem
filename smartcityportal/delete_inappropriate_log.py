import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcityportal.settings')
django.setup()

from accounts.models import AdminActivityLog

# Find and delete the inappropriate log entry
logs_to_delete = AdminActivityLog.objects.filter(
    description__icontains="Ramesh is pouring urine in cans"
)

if logs_to_delete.exists():
    count = logs_to_delete.count()
    print(f"Found {count} log(s) matching the criteria:")
    for log in logs_to_delete:
        print(f"  - ID: {log.id}")
        print(f"    Admin: {log.admin.username if log.admin else 'Unknown'}")
        print(f"    Action: {log.get_action_type_display()}")
        print(f"    Timestamp: {log.timestamp}")
        print(f"    Description: {log.description[:100]}...")
    
    logs_to_delete.delete()
    print(f"\n✓ Successfully deleted {count} inappropriate log entry(ies).")
else:
    print("No matching log entries found.")
