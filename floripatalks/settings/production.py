"""
Django production settings for Azure App Service.

Follows official Microsoft Azure App Service recommendations for Django.
"""

import os

from .base import *

# Security
DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set in production")

# ALLOWED_HOSTS - Official Azure pattern using WEBSITE_HOSTNAME
# Azure sets WEBSITE_HOSTNAME automatically (e.g., 'floripatalks-app.azurewebsites.net')
ALLOWED_HOSTS = [
    os.environ.get("WEBSITE_HOSTNAME", "127.0.0.1"),
]

# Add any additional hosts from environment variable (comma-separated)
# This allows custom domains to be added via Azure App Settings
additional_hosts = os.environ.get("ALLOWED_HOSTS", "").strip()
if additional_hosts:
    ALLOWED_HOSTS.extend([host.strip() for host in additional_hosts.split(",") if host.strip()])

# Remove duplicates
ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))

# Security settings for production
# Azure App Service terminates SSL at the load balancer, so we trust proxy headers
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# Azure handles HTTPS redirection at the platform level (via httpsOnly setting)
# Disable Django's redirect to avoid double-redirects
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
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

# Static files - Django's default storage (Azure App Service serves static files directly)

# Media files (use Azure Blob Storage in production if needed)
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
