"""
Custom middleware for FloripaTalks.

This middleware handles Azure App Service proxy headers, specifically the X-Forwarded-Proto header
that Azure should set automatically but may be missing for health checks.

Official References:
- Django: https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header
- Azure: Health checks from internal IPs may not include X-Forwarded-Proto header
"""

import logging
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


class AzureProxyHeaderMiddleware:
    """
    Middleware to handle Azure App Service proxy headers.

    Azure App Service terminates SSL at the load balancer and forwards requests as HTTP
    to the Django app. Azure should automatically set the X-Forwarded-Proto header, but
    health checks from internal IPs may not include this header.

    This middleware ensures the header is set when missing, allowing Django's
    SECURE_PROXY_SSL_HEADER setting to work correctly.

    Based on official recommendations:
    - Django docs: SECURE_PROXY_SSL_HEADER is the standard solution
    - Azure docs: Health checks may need special handling
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Azure internal health check IPs (link-local addresses)
        # These are safe to allow as they're only accessible from within Azure's network
        azure_internal_ips = [
            "169.254.129.1",
            "169.254.129.3",
            "169.254.129.4",
            "169.254.129.5",
        ]

        # Get the client IP from META (Django's standard way)
        # HTTP_X_FORWARDED_FOR can contain multiple IPs (comma-separated), take the first one
        client_ip = (
            request.headers.get("x-forwarded-for", "").split(",")[0].strip()
            or request.headers.get("x-real-ip", "")
            or request.META.get("REMOTE_ADDR", "")
        )

        # Check if X-Forwarded-Proto header exists in META (Django's SECURE_PROXY_SSL_HEADER looks here)
        has_proto_header = "x-forwarded-proto" in request.headers
        proto_value = request.headers.get("x-forwarded-proto", "NOT SET")
        is_health_check = client_ip in azure_internal_ips

        # Debug logging
        logger.info(
            f"🔍 AzureProxyHeaderMiddleware: "
            f"path={request.path}, "
            f"client_ip={client_ip}, "
            f"is_health_check={is_health_check}, "
            f"has_proto_header={has_proto_header}, "
            f"proto_value={proto_value}, "
            f"REMOTE_ADDR={request.META.get('REMOTE_ADDR', 'NOT SET')}, "
            f"HTTP_X_FORWARDED_FOR={request.headers.get('x-forwarded-for', 'NOT SET')}"
        )

        # Only set X-Forwarded-Proto header for Azure health checks (internal IPs)
        # Django's SECURE_PROXY_SSL_HEADER looks for HTTP_X_FORWARDED_PROTO in request.META
        #
        # Why only health checks?
        # 1. Azure should set it automatically for regular web requests
        # 2. Health checks from internal IPs may not include it
        # 3. Setting it for ALL requests (like Azure CLI commands) causes redirect loops
        # 4. For non-health-check requests without the header, let Django handle it naturally
        if not has_proto_header and is_health_check:
            # Health checks don't include the header, so we set it to prevent redirects
            request.META["HTTP_X_FORWARDED_PROTO"] = "https"
            logger.info(f"✅ Set HTTP_X_FORWARDED_PROTO=https for health check from {client_ip}")
        elif not has_proto_header:
            logger.warning(
                f"⚠️  Missing HTTP_X_FORWARDED_PROTO header for non-health-check request "
                f"from {client_ip} - Django may redirect"
            )

        response = self.get_response(request)
        return response
