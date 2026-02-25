.venv\Scripts\python.exe manage.py migrate accounts > migration_output.log 2>&1
echo === Migration Output ===
type migration_output.log
echo.
echo === Checking Migration Status ===
.venv\Scripts\python.exe manage.py showmigrations accounts
