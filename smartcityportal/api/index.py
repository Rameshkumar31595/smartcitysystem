import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcityportal.settings')

import django
django.setup()

# Import the WSGI application
from django.core.wsgi import get_wsgi_application

# This is the WSGI application that Vercel will use
app = get_wsgi_application()
