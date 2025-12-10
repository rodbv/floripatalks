"""
Django development settings for floripatalks project.
"""

import os

from dotenv import load_dotenv

from .base import *

# Add development-only apps
INSTALLED_APPS += [
    "django_browser_reload",  # Hot-reload for development
    "django_extensions",  # Enhanced Django management commands (shell_plus, etc.)
]

# django-extensions configuration
SHELL_PLUS = "ipython"
SHELL_PLUS_PRINT_SQL = True

# Load environment variables from .env file
# This allows using .env file for local development
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded environment variables from {env_path}")
else:
    print(f"ℹ️  No .env file found at {env_path}, using system environment variables")

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Database - SQLite for development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# OAuth credentials from environment variables (for development)
# Set these in your environment or .env file:
# export GOOGLE_CLIENT_ID="your-google-client-id"
# export GOOGLE_CLIENT_SECRET="your-google-client-secret"
if os.environ.get("GOOGLE_CLIENT_ID"):
    SOCIALACCOUNT_PROVIDERS["google"]["APP"]["client_id"] = os.environ.get("GOOGLE_CLIENT_ID")
    SOCIALACCOUNT_PROVIDERS["google"]["APP"]["secret"] = os.environ.get("GOOGLE_CLIENT_SECRET")
