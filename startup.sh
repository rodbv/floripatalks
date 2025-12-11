#!/bin/bash
# Azure App Service startup script for FloripaTalks Django application
#
# This script runs when Azure App Service starts your application.
# It ensures dependencies are installed, database migrations are applied, and starts the web server.

# Don't exit on error immediately - we want to log errors
set +e

echo "🚀 Starting FloripaTalks application..."
echo "📅 Timestamp: $(date)"

# Change to app directory (Azure deploys to /home/site/wwwroot)
cd /home/site/wwwroot || cd "$(dirname "$0")"
echo "📂 Working directory: $(pwd)"

# Check for required environment variables
echo "🔍 Checking environment variables..."
if [ -z "$SECRET_KEY" ]; then
    echo "❌ ERROR: SECRET_KEY environment variable is not set!"
    echo "   Please set SECRET_KEY in Azure App Service Configuration → Application settings"
    exit 1
fi

if [ -z "$GOOGLE_CLIENT_ID" ] || [ -z "$GOOGLE_CLIENT_SECRET" ]; then
    echo "❌ ERROR: GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET environment variable is not set!"
    echo "   Please set these in Azure App Service Configuration → Application settings"
    exit 1
fi

if [ -z "$DJANGO_SETTINGS_MODULE" ]; then
    echo "⚠️  WARNING: DJANGO_SETTINGS_MODULE not set, defaulting to production"
    export DJANGO_SETTINGS_MODULE=floripatalks.settings.production
fi

echo "✅ Environment variables check passed"

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ ERROR: Python not found!"
    exit 1
fi
echo "🐍 Using Python: $PYTHON_CMD ($($PYTHON_CMD --version))"

# Check if Django is installed (dependencies should be installed during deployment)
# Only install if missing (fallback for cases where Azure didn't install them)
if ! $PYTHON_CMD -c "import django" 2>/dev/null; then
    echo "⚠️  Django not found - installing dependencies from requirements.txt..."
    if [ -f "requirements.txt" ]; then
        pip install --no-cache-dir -r requirements.txt
        if [ $? -eq 0 ]; then
            echo "   ✅ Dependencies installed successfully"
        else
            echo "   ❌ ERROR: Failed to install dependencies!"
            exit 1
        fi
    else
        echo "   ❌ ERROR: requirements.txt not found!"
        exit 1
    fi
else
    echo "✅ Dependencies already installed (skipping installation)"
fi

# Run database migrations (required - not done in CI/CD)
echo "📦 Running database migrations..."
$PYTHON_CMD manage.py migrate --noinput
if [ $? -ne 0 ]; then
    echo "❌ ERROR: Database migrations failed!"
    echo "   Check the error messages above for details"
    exit 1
fi
echo "   ✅ Migrations completed"

# Collect static files (already done in CI/CD, but ensures they're present on restart)
echo "📁 Collecting static files..."
$PYTHON_CMD manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "❌ ERROR: Static file collection failed!"
    echo "   Check the error messages above for details"
    exit 1
fi
echo "   ✅ Static files collected"

# Start Gunicorn web server (production-ready WSGI server)
echo "🌐 Starting Gunicorn web server..."
echo "   Binding to: 0.0.0.0:8000"
echo "   Workers: 2"
echo "   Timeout: 120s"

# Use exec to replace shell process with Gunicorn
exec gunicorn floripatalks.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
