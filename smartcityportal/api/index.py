import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcityportal.settings')

# Initialize Django before importing anything else
import django
django.setup()

# Import WSGI application
from smartcityportal.wsgi import application

# Export for Vercel - it will handle the WSGI interface
app = application
