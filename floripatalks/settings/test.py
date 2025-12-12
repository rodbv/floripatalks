"""
Django test settings for floripatalks project.

Uses in-memory SQLite for faster test execution.
"""

from .base import *

# Override STORAGES FIRST before any other imports that might use it
# This ensures WhiteNoise storage is not used in tests
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Use in-memory SQLite for tests - much faster than disk-based
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


# Disable migrations during tests for speed
# Migrations are tested separately
class DisableMigrations:
    def __contains__(self, item: str) -> bool:
        return True

    def __getitem__(self, item: str) -> None:
        return None


MIGRATION_MODULES = DisableMigrations()

# Speed up password hashing for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable email sending in tests
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Disable logging during tests for cleaner output
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "root": {
        "handlers": ["null"],
    },
}

# STORAGES already overridden above to use StaticFilesStorage (not WhiteNoise)

# Remove WhiteNoise middleware in tests - it requires a manifest file
# Use Django's default static file serving instead
MIDDLEWARE = [mw for mw in MIDDLEWARE if mw != "whitenoise.middleware.WhiteNoiseMiddleware"]
