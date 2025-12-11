"""
Custom middleware for FloripaTalks.

Sets X-Forwarded-Proto header if missing to prevent redirect loops with Azure App Service.
"""

import logging
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


class AzureProxyHeaderMiddleware:
    """
    Sets X-Forwarded-Proto header if missing to prevent redirect loops.

    Azure App Service terminates SSL at the load balancer. Azure should set
    X-Forwarded-Proto automatically, but if it's missing, Django may treat
    HTTPS requests as HTTP and redirect, causing loops. This middleware sets
    the header for all requests if missing.
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
        client_ip = request.META.get("REMOTE_ADDR", "N/A")

        if not has_header:
            request.META["HTTP_X_FORWARDED_PROTO"] = "https"
            logger.info(
                f"🔧 AzureProxyHeaderMiddleware: Set HTTP_X_FORWARDED_PROTO=https for {request.path} "
                f"(client_ip={client_ip}, scheme={request_scheme}, is_secure={is_secure})"
            )
        else:
            logger.debug(
                f"✅ AzureProxyHeaderMiddleware: Header already set for {request.path} "
                f"(value={header_value}, client_ip={client_ip}, scheme={request_scheme}, is_secure={is_secure})"
            )

        response = self.get_response(request)
        return response
