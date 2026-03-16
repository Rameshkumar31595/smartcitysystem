import os
import sys
from pathlib import Path

# Detect Django project root for both deployment modes:
# 1) repo-root deploy: smartcityportal/api/index.py
# 2) subfolder deploy root: api/index.py
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = None

for parent in CURRENT_FILE.parents:
    if (parent / "manage.py").exists() and (parent / "smartcityportal" / "settings.py").exists():
        PROJECT_ROOT = parent
        break

if PROJECT_ROOT is None:
    raise RuntimeError("Unable to locate Django project root from api/index.py")

sys.path.insert(0, str(PROJECT_ROOT))

# Use the actual Django settings module package at PROJECT_ROOT/smartcityportal/settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartcityportal.settings")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()