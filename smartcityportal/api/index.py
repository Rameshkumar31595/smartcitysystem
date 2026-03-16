import os
import sys
from pathlib import Path

# Resolve Django project root robustly for both deployment layouts:
# - repo-root deploy: smartcityportal/api/index.py
# - subfolder deploy: api/index.py
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = None

for parent in CURRENT_FILE.parents:
	if (parent / "manage.py").exists() and (parent / "smartcityportal" / "settings.py").exists():
		PROJECT_ROOT = parent
		break

if PROJECT_ROOT is None:
	raise RuntimeError("Unable to locate Django project root from api/index.py")

sys.path.insert(0, str(PROJECT_ROOT))

# settings.py is located at <project-root>/smartcityportal/settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartcityportal.settings")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()