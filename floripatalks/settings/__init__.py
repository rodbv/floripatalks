"""
Django settings package with automatic environment detection.

Auto-detects production if WEBSITE_HOSTNAME is set (Azure App Service).
Otherwise defaults to development.
"""

import os

# If WEBSITE_HOSTNAME is set, we're in Azure App Service (production)
if os.environ.get("WEBSITE_HOSTNAME"):
    from .production import *  # noqa: F403, F401
else:
    # Default to development (local development)
    from .development import *  # noqa: F403, F401
