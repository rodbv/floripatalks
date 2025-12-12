"""
Django settings package with automatic environment detection.

Common cloud deployment pattern (used by Heroku, AWS, Azure, etc.):
- Production: Auto-detects via WEBSITE_HOSTNAME (Azure) or DJANGO_ENV=production
- Test: If DJANGO_SETTINGS_MODULE is explicitly set to test settings
- Development: Default fallback for local development

You can still override by explicitly setting DJANGO_SETTINGS_MODULE.
"""

import os

# Check if DJANGO_SETTINGS_MODULE is explicitly set (highest priority)
explicit_settings = os.environ.get("DJANGO_SETTINGS_MODULE", "")

# If explicitly set to test settings, use test
if explicit_settings.endswith(".test"):
    from .test import *  # noqa: F403, F401
# If explicitly set to production, use production
elif explicit_settings.endswith(".production"):
    from .production import *  # noqa: F403, F401
# If explicitly set to development, use development
elif explicit_settings.endswith(".development"):
    from .development import *  # noqa: F403, F401
# Auto-detect environment (cloud platform pattern)
elif os.environ.get("WEBSITE_HOSTNAME") or os.environ.get("DJANGO_ENV") == "production":
    # Azure App Service sets WEBSITE_HOSTNAME automatically
    # Heroku, AWS, and other platforms use similar patterns
    # Or explicitly set DJANGO_ENV=production
    from .production import *  # noqa: F403, F401
else:
    # Default to development (local development)
    from .development import *  # noqa: F403, F401
