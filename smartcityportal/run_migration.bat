@echo off
echo Applying migration for AdminActivityLog...
python manage.py migrate accounts
echo.
echo Checking migration status...
python manage.py showmigrations accounts
echo.
echo Done! Please restart your Django development server.
pause
