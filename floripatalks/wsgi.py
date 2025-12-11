"""
WSGI config for floripatalks project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use production settings by default, but allow override via environment variable
# This ensures production settings are used even if DJANGO_SETTINGS_MODULE isn't set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "floripatalks.settings.production")

application = get_wsgi_application()
