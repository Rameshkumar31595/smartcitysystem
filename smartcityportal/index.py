import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

# Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcityportal.settings')

# Import and setup Django first
import django
django.setup()

# Now import the app
from smartcityportal.wsgi import application

# This is what Vercel will use
app = application

# Handler for Vercel
def handler(request, response):
    return app(request, response)
