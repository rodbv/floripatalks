#!/bin/bash
# Azure App Service startup script for Django application
#
# Official Microsoft-recommended pattern for Django on Azure App Service
# https://learn.microsoft.com/en-us/azure/developer/python/configure-python-web-app-on-app-service

set -e

# Run database migrations (only unapplied migrations will run)
# Django's migrate command is idempotent - it only applies migrations that haven't been applied yet
# If all migrations are already applied, this command does nothing
python manage.py migrate --noinput

# Collect static files (WhiteNoise will serve them)
# Note: Oryx build system may do this automatically, but explicit is cleaner
python manage.py collectstatic --noinput

# Start Gunicorn (official WSGI server for Django)
# Azure sets $PORT environment variable automatically
# Using '-' for log files ensures logs are captured by Azure
exec gunicorn floripatalks.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 600 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info
