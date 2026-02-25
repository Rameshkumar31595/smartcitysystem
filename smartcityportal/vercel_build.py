#!/usr/bin/env python
"""
Vercel build script for Django
This runs during deployment to collect static files
"""
import os
import sys
import subprocess

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcityportal.settings')

print("=" * 50)
print("Starting Vercel build process...")
print("=" * 50)

try:
    # Collect static files
    print("\n📦 Collecting static files...")
    result = subprocess.run(
        [sys.executable, 'manage.py', 'collectstatic', '--noinput', '--clear'],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"⚠️ Warning: collectstatic failed: {result.stderr}")
    else:
        print("✅ Static files collected successfully")
    
    print("\n✅ Build completed successfully!")
    print("=" * 50)
    
except Exception as e:
    print(f"\n❌ Build failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
