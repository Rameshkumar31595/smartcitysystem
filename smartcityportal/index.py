import os
from django.core.wsgi import get_wsgi_application

# Tell Django where to find the settings file
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartcityportal.settings")

# Vercel's Python builder specifically looks for a variable named 'app'
app = get_wsgi_application()
