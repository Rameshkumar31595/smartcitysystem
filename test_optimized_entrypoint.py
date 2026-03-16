#!/usr/bin/env python
import sys
import importlib.util
from pathlib import Path

api_path = Path('smartcityportal/api/index_optimized.py').resolve()
print(f'Testing: {api_path}')
print()

spec = importlib.util.spec_from_file_location('api_optimized', str(api_path))
module = importlib.util.module_from_spec(spec)

try:
    print('Loading optimized entrypoint...')
    spec.loader.exec_module(module)
    print('✓ Module loaded successfully')
    print(f'✓ Has app: {hasattr(module, "app")}')
    print(f'✓ app callable: {callable(module.app)}')
    print()
    print('SUCCESS: Optimized entrypoint is ready')
except Exception as e:
    print(f'✗ Failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
