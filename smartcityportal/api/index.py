import os
import sys
from pathlib import Path

# Go to project root
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

# Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartcityportal.settings")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()