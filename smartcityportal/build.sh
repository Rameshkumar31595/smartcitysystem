#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Build completed successfully!"
