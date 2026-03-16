#!/usr/bin/env python
"""Test script to verify Vercel entrypoint loads correctly."""
import sys
from pathlib import Path
import importlib.util

# Simulate dynamic import of api/index.py
api_path = Path('smartcityportal/api/index.py').resolve()
print(f'API Path: {api_path}')
print(f'API Path Exists: {api_path.exists()}')
print()

# Try to import it
spec = importlib.util.spec_from_file_location('api_index', str(api_path))
module = importlib.util.module_from_spec(spec)

try:
    print('Attempting to load module...')
    spec.loader.exec_module(module)
    print('✓ Module loaded successfully')
    print(f'✓ Has app attribute: {hasattr(module, "app")}')
    if hasattr(module, 'app'):
        print(f'✓ app type: {type(module.app)}')
        print(f'✓ app callable: {callable(module.app)}')
    print()
    print('SUCCESS: Entrypoint is ready for Vercel deployment')
except Exception as e:
    print(f'✗ Import failed: {type(e).__name__}: {e}')
    import traceback
    print()
    print('Full traceback:')
    traceback.print_exc()
    sys.exit(1)
