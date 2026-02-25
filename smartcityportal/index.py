import os
import sys

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcityportal.settings')

# Import Django and setup
import django
django.setup()

# Import the WSGI application
from smartcityportal.wsgi import application

# Vercel expects "app" as the WSGI application
app = application
