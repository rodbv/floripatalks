#!/bin/bash
# Azure App Service startup script for Django application
#
# Official Microsoft-recommended pattern for Django on Azure App Service
# https://learn.microsoft.com/en-us/azure/developer/python/configure-python-web-app-on-app-service

set -e

# Ensure /home/site/data/ directory exists with correct permissions
# This directory persists across deployments and is where we store the SQLite database
# /home/site/wwwroot/ gets overwritten on each deployment, but /home/site/data/ persists
# Using /home/site/data/ (within /home/site/ which exists by default) instead of /home/data/
echo "Checking /home/site/data directory..."
if [ ! -d "/home/site/data" ]; then
    echo "Creating /home/site/data directory..."
    mkdir -p /home/site/data
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create /home/site/data directory"
        exit 1
    fi
    chmod 755 /home/site/data
    echo "✅ Created /home/site/data directory for SQLite database"
else
    echo "✅ /home/site/data directory already exists"
fi

# Verify we can write to the directory
if [ ! -w "/home/site/data" ]; then
    echo "ERROR: Cannot write to /home/site/data directory"
    ls -ld /home/site/data
    exit 1
fi
echo "✅ /home/site/data is writable"

# Run database migrations (only unapplied migrations will run)
# Django's migrate command is idempotent - it only applies migrations that haven't been applied yet
# If all migrations are already applied, this command does nothing
# Note: Database file stored in /home/site/data/ which persists across deployments
# /home/site/wwwroot/ gets overwritten on each deployment, but /home/site/data/ persists
python manage.py migrate --noinput --verbosity=0

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
