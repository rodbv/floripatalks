#!/bin/bash
# Azure App Service startup script for FloripaTalks Django application
#
# This script runs when Azure App Service starts your application.
# It ensures dependencies are installed, database migrations are applied, and starts the web server.

set -e  # Exit on error

echo "🚀 Starting FloripaTalks application..."

# Change to app directory (Azure deploys to /home/site/wwwroot)
cd /home/site/wwwroot || cd "$(dirname "$0")"

# Install dependencies if requirements.txt exists and packages aren't installed
# Azure usually auto-installs from requirements.txt, but this ensures they're present
if [ -f "requirements.txt" ]; then
    echo "📦 Checking/installing dependencies from requirements.txt..."
    # Check if Django is installed, if not, install all dependencies
    if ! python -c "import django" 2>/dev/null; then
        echo "   Installing dependencies (Django not found)..."
        pip install --no-cache-dir -r requirements.txt
    else
        echo "   Dependencies already installed ✓"
    fi
fi

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
