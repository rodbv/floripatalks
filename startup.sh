#!/bin/bash
# Azure App Service startup script for FloripaTalks Django application
#
# This script runs when Azure App Service starts your application.
# It ensures database migrations are applied and starts the web server.

set -e  # Exit on error

echo "🚀 Starting FloripaTalks application..."

# Run database migrations (required - not done in CI/CD)
echo "📦 Running database migrations..."
python manage.py migrate --noinput

# Collect static files (already done in CI/CD, but ensures they're present on restart)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn web server (production-ready WSGI server)
# Note: Gunicorn should be added to pyproject.toml dependencies for production
echo "🌐 Starting Gunicorn web server..."
exec gunicorn floripatalks.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
