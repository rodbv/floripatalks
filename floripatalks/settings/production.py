"""
Django production settings for Azure App Service.
"""

import os

from .base import *

# Security
DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set in production")

ALLOWED_HOSTS = [
    host.strip() for host in os.environ.get("ALLOWED_HOSTS", "").split(",") if host.strip()
]

# Security settings for production
SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS
SESSION_COOKIE_SECURE = True  # Only send cookies over HTTPS
CSRF_COOKIE_SECURE = True  # Only send CSRF cookies over HTTPS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Database (SQLite)
# SQLite database stored in persistent storage (/home/site/wwwroot/)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Note: Azure App Service persistent storage ensures database survives restarts

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# Don't use STATICFILES_DIRS in production - all static files should be collected to STATIC_ROOT

# Media files (use Azure Blob Storage in production)
# Install: django-storages[azure]
# DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"
# AZURE_ACCOUNT_NAME = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME")
# AZURE_ACCOUNT_KEY = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")
# AZURE_CONTAINER = "media"

# Email (use Azure Communication Services or SendGrid)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# Configure SMTP settings via environment variables:
# EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS

# OAuth credentials from environment variables (required in production)
if os.environ.get("GOOGLE_CLIENT_ID"):
    SOCIALACCOUNT_PROVIDERS["google"]["APP"]["client_id"] = os.environ.get("GOOGLE_CLIENT_ID")
    SOCIALACCOUNT_PROVIDERS["google"]["APP"]["secret"] = os.environ.get("GOOGLE_CLIENT_SECRET")
else:
    raise ValueError("GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in production")

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
