"""
Custom middleware for FloripaTalks.

Handles Azure App Service proxy headers for health checks that don't include X-Forwarded-Proto.
"""

from collections.abc import Callable

from django.http import HttpRequest, HttpResponse


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
        # Azure internal health check IPs (link-local addresses)
        # These are safe to allow as they're only accessible from within Azure's network
        azure_internal_ips = [
            "169.254.129.1",
            "169.254.129.3",
            "169.254.129.4",
            "169.254.129.5",
        ]

        # Get the client IP from META (Django's standard way)
        client_ip = (
            request.headers.get("x-forwarded-for", "").split(",")[0].strip()
            or request.headers.get("x-real-ip", "")
            or request.META.get("REMOTE_ADDR", "")
        )

        # Only set X-Forwarded-Proto header for Azure health checks (internal IPs)
        # Azure should set this automatically for regular requests, but health checks may not include it
        if "x-forwarded-proto" not in request.headers and client_ip in azure_internal_ips:
            request.META["HTTP_X_FORWARDED_PROTO"] = "https"

        response = self.get_response(request)
        return response
