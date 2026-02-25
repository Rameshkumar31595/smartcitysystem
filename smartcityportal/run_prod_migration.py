import os
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_F5LiZCYSu7no@ep-muddy-forest-ai0h6zx7-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require'
os.environ['DJANGO_SETTINGS_MODULE'] = 'smartcityportal.settings'

import django
django.setup()

from django.core.management import call_command

print("\n" + "="*70)
print("Running migrations on Neon production database...")
print("="*70 + "\n")

call_command('migrate')

print("\n" + "="*70)
print("✅ Migrations completed successfully!")
print("="*70)
