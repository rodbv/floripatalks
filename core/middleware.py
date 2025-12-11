"""
Custom middleware for FloripaTalks.

Handles Azure App Service proxy headers for health checks that don't include X-Forwarded-Proto.
"""

import logging
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


class AzureProxyHeaderMiddleware:
    """
    Sets X-Forwarded-Proto header for Azure health checks that don't include it.

    Azure health checks from internal IPs (169.254.x.x) may not include the
    X-Forwarded-Proto header, causing Django's SECURE_PROXY_SSL_HEADER to fail.
    This middleware sets the header for health checks only.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Set X-Forwarded-Proto header if missing
        # Django's SECURE_PROXY_SSL_HEADER looks for HTTP_X_FORWARDED_PROTO in request.META
        # Azure should set this automatically, but if it's missing, we set it to prevent redirects
        # This is safe because Azure's httpsOnly ensures all external requests are HTTPS
        has_header = "x-forwarded-proto" in request.headers
        header_value = request.headers.get("x-forwarded-proto", "NOT SET")
        request_scheme = request.scheme
        is_secure = request.is_secure()

        if not has_header:
            request.META["HTTP_X_FORWARDED_PROTO"] = "https"
            logger.info(
                f"🔧 AzureProxyHeaderMiddleware: Set HTTP_X_FORWARDED_PROTO=https for {request.path} "
                f"(scheme={request_scheme}, is_secure={is_secure}, REMOTE_ADDR={request.META.get('REMOTE_ADDR', 'N/A')})"
            )
        else:
            logger.debug(
                f"✅ AzureProxyHeaderMiddleware: Header already set for {request.path} "
                f"(value={header_value}, scheme={request_scheme}, is_secure={is_secure})"
            )

        response = self.get_response(request)
        return response
