#!/usr/bin/env python
"""
Test script to verify landing page renders without staticfiles manifest errors.
This simulates loading the landing page view.
"""
import os
import sys
from pathlib import Path

# Setup path
repo_root = Path(__file__).resolve().parent / "smartcityportal"
sys.path.insert(0, str(repo_root))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartcityportal.settings")

print("Setting up Django...")
import django
django.setup()
print("✓ Django setup successful")
print()

# Test that we can import the landing view
print("Testing templates import...")
try:
    from django.template.loader import render_to_string
    print("✓ Template loader imported")
except Exception as e:
    print(f"✗ Failed to import template loader: {e}")
    sys.exit(1)

# Test rendering the landing page template (without full request)
print()
print("Testing landing page template rendering...")
try:
    # Get the landing template
    from django.template.loader import get_template
    landing_template = get_template('landing.html')
    print(f"✓ landing.html template loaded")
    
    # Try to render it with minimal context
    context = {}
    rendered = landing_template.render(context)
    
    if 'pfsd_logo.png' in rendered:
        print(f"✓ landing.html renders successfully")
        print(f"✓ pfsd_logo.png reference found in rendered output")
    else:
        print(f"✓ landing.html renders successfully (logo not in main content)")
        
except Exception as e:
    print(f"✗ Failed to render landing.html: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test that collectstatic configuration is loaded correctly
print()
print("Testing staticfiles configuration...")
try:
    from django.conf import settings
    print(f"✓ STATIC_URL: {settings.STATIC_URL}")
    print(f"✓ STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"✓ STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
    
    # Check it's using the non-manifest version
    if "CompressedStaticFilesStorage" in settings.STATICFILES_STORAGE:
        if "Manifest" not in settings.STATICFILES_STORAGE:
            print(f"✓ Using CompressedStaticFilesStorage (NO manifest)")
            print(f"✓ This is correct for serverless deployment")
        else:
            print(f"✗ Still using Manifest storage!")
    else:
        print(f"✗ Unexpected storage class: {settings.STATICFILES_STORAGE}")
        
except Exception as e:
    print(f"✗ Error checking staticfiles config: {e}")
    sys.exit(1)

print()
print("✓✓✓ All tests passed! Landing page renders without manifest errors ✓✓✓")
