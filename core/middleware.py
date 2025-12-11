"""
Custom middleware for FloripaTalks.

This middleware handles Azure App Service proxy headers, specifically the X-Forwarded-Proto header
that Azure should set automatically but may be missing for health checks.

Official References:
- Django: https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header
- Azure: Health checks from internal IPs may not include X-Forwarded-Proto header
"""

from collections.abc import Callable

from django.http import HttpRequest, HttpResponse


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

        # Get the client IP
        client_ip = (
            request.headers.get("x-forwarded-for", "").split(",")[0].strip()
            or request.headers.get("x-real-ip", "")
            or request.META.get("REMOTE_ADDR", "")
        )

        # If X-Forwarded-Proto header is missing, set it based on context
        # Azure should set this automatically, but health checks may not include it
        if "x-forwarded-proto" not in request.headers:
            # For Azure health checks (internal IPs), set to "https" to prevent redirects
            # Health checks should work without redirects, so we mark them as HTTPS
            # This is a workaround for Azure health checks that don't include the header
            if client_ip in azure_internal_ips:
                request.META["HTTP_X_FORWARDED_PROTO"] = "https"
            else:
                # For regular requests, Azure should set this header automatically
                # If it's missing, assume HTTPS (Azure App Service uses HTTPS by default)
                # This is a fallback in case Azure doesn't set the header for some reason
                request.META["HTTP_X_FORWARDED_PROTO"] = "https"

        response = self.get_response(request)
        return response
