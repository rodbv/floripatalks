"""
Django production settings for Azure App Service.
"""

import os

from .base import *

# Remove development-only apps from INSTALLED_APPS if they were added
# (This ensures clean production settings even if development.py was imported)
if "django_browser_reload" in INSTALLED_APPS:
    INSTALLED_APPS.remove("django_browser_reload")
if "django_extensions" in INSTALLED_APPS:
    INSTALLED_APPS.remove("django_extensions")

# Security
DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set in production")

# ALLOWED_HOSTS from environment variable
# Format: "host1.com,host2.com" or single host
allowed_hosts_str = os.environ.get("ALLOWED_HOSTS", "").strip()
ALLOWED_HOSTS = (
    [host.strip() for host in allowed_hosts_str.split(",") if host.strip()]
    if allowed_hosts_str
    else []
)

# Always allow Azure internal IPs for health checks
# Azure health checks use internal IPs in the 169.254.x.x range (link-local addresses)
# These are safe to allow as they're only accessible from within Azure's network
azure_internal_ips = [
    "169.254.129.1",  # Common Azure health check IP
    "169.254.129.3",  # Common Azure health check IP (from error)
    "169.254.129.4",  # Common Azure health check IP
]
ALLOWED_HOSTS.extend(azure_internal_ips)
ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))  # Remove duplicates

if not allowed_hosts_str:
    print("⚠️  WARNING: ALLOWED_HOSTS not set in environment variables!")
    print("   Please set ALLOWED_HOSTS in Azure App Service Configuration → Application settings")
else:
    print(
        f"✅ ALLOWED_HOSTS configured: {len(ALLOWED_HOSTS)} host(s) (includes Azure health check IPs)"
    )

# Security settings for production
# Azure App Service terminates SSL at the load balancer, so we need to trust proxy headers
# This tells Django that Azure's load balancer is handling HTTPS termination
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Redirect HTTP to HTTPS (Azure handles this, but this is a safety measure)
SECURE_SSL_REDIRECT = True
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
