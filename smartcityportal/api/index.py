"""
Vercel Entrypoint - Production-Ready Django WSGI Handler

This module serves as the entry point for Vercel's Python serverless runtime.
It properly initializes the Django application and exports a WSGI handler.

Key aspects:
- Auto-detects Django project root for reliability
- Sets up Python path correctly for nested project structure
- Initializes Django with proper error handling
- Returns a WSGI-compatible handler for serverless requests
"""
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# 1. DETERMINE PROJECT ROOT
# ============================================================================
# The entry point is at: /repo/smartcityportal/api/index.py
# We need to add /repo/smartcityportal to sys.path
# So Django can import: smartcityportal.settings

ENTRY_POINT_FILE = Path(__file__).resolve()
PROJECT_BASE = ENTRY_POINT_FILE.parent.parent  # Goes up from api/ to smartcityportal/

logger.info(f"Entry point: {ENTRY_POINT_FILE}")
logger.info(f"Project base: {PROJECT_BASE}")

# Verify the expected Django structure exists
DJANGO_PACKAGE = PROJECT_BASE / "smartcityportal"
MANAGE_PY = PROJECT_BASE / "manage.py"
SETTINGS_MODULE = DJANGO_PACKAGE / "settings.py"

if not DJANGO_PACKAGE.exists():
    raise RuntimeError(
        f"Django package not found at {DJANGO_PACKAGE}. "
        f"Expected structure: smartcityportal/smartcityportal/settings.py"
    )

if not MANAGE_PY.exists():
    raise RuntimeError(
        f"manage.py not found at {MANAGE_PY}. "
        f"Expected: smartcityportal/manage.py"
    )

if not SETTINGS_MODULE.exists():
    raise RuntimeError(
        f"settings.py not found at {SETTINGS_MODULE}. "
        f"Expected: smartcityportal/smartcityportal/settings.py"
    )

logger.info(f"✓ Django structure verified")

# ============================================================================
# 2. CONFIGURE PYTHON PATH
# ============================================================================
# Add project base to sys.path so Python can find 'smartcityportal' package
if str(PROJECT_BASE) not in sys.path:
    sys.path.insert(0, str(PROJECT_BASE))
    logger.info(f"Added to sys.path: {PROJECT_BASE}")

# ============================================================================
# 3. CONFIGURE DJANGO
# ============================================================================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartcityportal.settings")

logger.info(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

# ============================================================================
# 4. INITIALIZE DJANGO AND GET WSGI APP
# ============================================================================
try:
    from django.core.wsgi import get_wsgi_application
    
    logger.info("Importing Django WSGI handler...")
    app = get_wsgi_application()
    logger.info("✓ Django WSGI app initialized successfully")
    
except ImportError as e:
    logger.error(f"Failed to import Django: {e}")
    raise RuntimeError(
        "Django import failed. Ensure Django >= 4.2 is installed in requirements.txt"
    ) from e
    
except Exception as e:
    logger.error(f"Failed to initialize Django WSGI app: {e}")
    raise RuntimeError(
        f"Django initialization failed: {type(e).__name__}: {e}"
    ) from e

# ============================================================================
# WSGI APP EXPORT (for Vercel)
# ============================================================================
# Vercel runtime expects a callable named 'app' at module level
# The 'app' should be a WSGI application (callable with environ, start_response)

if not callable(app):
    raise RuntimeError(f"WSGI app is not callable: {type(app)}")

logger.info("✓ Ready to handle Vercel requests")