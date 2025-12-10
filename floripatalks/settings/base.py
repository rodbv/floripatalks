"""
Django base settings for floripatalks project.

Shared settings for all environments.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# settings/base.py is in floripatalks/settings/, so we go up 2 levels to project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# This should be overridden in production.py
SECRET_KEY = "django-insecure-exegsz^ama3ctf6l-n2la9#gy&v6)m#11ude8z8hsf+1fn7zbj"

# Custom User Model
AUTH_USER_MODEL = "accounts.User"

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",  # Required for django-allauth
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "django_htmx",
    "django_cotton",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # Social providers
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.openid_connect",  # Used for LinkedIn
    # Local apps
    "events",
    "accounts",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "floripatalks.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # Required for allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "floripatalks.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django-allauth configuration
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

# Django-allauth account configuration
ACCOUNT_LOGIN_METHODS = {"email"}  # Use email for login
ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "password1*",
    "password2*",
]  # Email required, username not required
ACCOUNT_EMAIL_VERIFICATION = "none"  # For MVP, skip email verification
ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_ADAPTER = "accounts.adapters.CustomAccountAdapter"  # Optional: uncomment if custom adapter needed

# Django-allauth social account configuration
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"  # For MVP, skip email verification
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_STORE_TOKENS = False  # Don't store OAuth tokens (not needed for basic SSO)
# Allow direct redirect to OAuth provider without intermediate confirmation page
# Note: This uses GET instead of POST, which is acceptable when user explicitly clicks login button
SOCIALACCOUNT_LOGIN_ON_GET = True

# Social provider settings
# These will be configured via environment variables in production
# For development, set these in development.py or via environment variables
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "APP": {
            "client_id": "",  # Set via GOOGLE_CLIENT_ID environment variable
            "secret": "",  # Set via GOOGLE_CLIENT_SECRET environment variable
            "key": "",
        },
    },
    "openid_connect": {
        "APPS": [
            {
                "provider_id": "linkedin",
                "name": "LinkedIn",
                "client_id": "",  # Set via LINKEDIN_CLIENT_ID environment variable
                "secret": "",  # Set via LINKEDIN_CLIENT_SECRET environment variable
                "settings": {
                    "server_url": "https://www.linkedin.com/oauth",
                },
            }
        ]
    },
}

# Login/Logout URLs
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
