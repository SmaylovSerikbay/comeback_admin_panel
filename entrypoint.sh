#!/bin/bash
set -e
cd /app
echo "Running migrations..."
python manage.py migrate --noinput
echo "Creating users (admin/cashier)..."
python create_users.py
echo "Starting gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 comeback_admin.wsgi:application
