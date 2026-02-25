"""
Script to run migrations on Neon production database
"""
import os
import sys

print("\n" + "="*70)
print("PRODUCTION DATABASE MIGRATION SCRIPT")
print("="*70)

# Get DATABASE_URL from user
print("\nPaste your Neon DATABASE_URL here:")
print("(It should start with: postgresql://...)")
database_url = input("\nDATABASE_URL: ").strip()

if not database_url.startswith("postgresql://"):
    print("\n❌ Error: DATABASE_URL must start with 'postgresql://'")
    sys.exit(1)

# Set environment variable
os.environ['DATABASE_URL'] = database_url
os.environ['DJANGO_SETTINGS_MODULE'] = 'smartcityportal.settings'

print("\n" + "="*70)
print("Running migrations on production database...")
print("="*70 + "\n")

# Import Django
import django
django.setup()

# Run migrations
from django.core.management import call_command

try:
    # Show current migration status
    print("\n📋 Current migration status:")
    call_command('showmigrations')
    
    # Run migrations
    print("\n🚀 Applying migrations...")
    call_command('migrate')
    
    print("\n✅ Migrations completed successfully!")
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("\n1. Create a superuser for production:")
    print("   Run this script again or use: python manage.py createsuperuser")
    print("\n2. Your deployment should now work!")
    print("   Visit: https://smartcitysystem.vercel.app")
    print("\n" + "="*70)
    
except Exception as e:
    print(f"\n❌ Error running migrations: {e}")
    sys.exit(1)
