"""
Custom middleware for FloripaTalks.

Sets X-Forwarded-Proto header if missing to prevent redirect loops with Azure App Service.
"""

import logging
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)

# Print at module load to confirm middleware is being imported
print("✅ AzureProxyHeaderMiddleware module loaded", flush=True)


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
        try:
            # Log that middleware is running (to confirm it's being called)
            # Use both logger and print to ensure we see it
            log_msg = (
                f"🚀 AzureProxyHeaderMiddleware: Processing {request.method} {request.path} "
                f"(REMOTE_ADDR={request.META.get('REMOTE_ADDR', 'N/A')})"
            )
            logger.info(log_msg)
            print(log_msg, flush=True)  # Also print to stdout (Azure logs stdout/stderr)

            # Set X-Forwarded-Proto header if missing
            # Django's SECURE_PROXY_SSL_HEADER looks for HTTP_X_FORWARDED_PROTO in request.META
            # Azure should set this automatically, but if it's missing, we set it to prevent redirects
            # This is safe because Azure's httpsOnly ensures all external requests are HTTPS
            # IMPORTANT: Check request.META, not request.headers (Django uses META for these headers)
            has_header = "x-forwarded-proto" in request.headers
            header_value = request.headers.get("x-forwarded-proto", "NOT SET")
            request_scheme = request.scheme
            is_secure = request.is_secure()
            client_ip = request.META.get("REMOTE_ADDR", "N/A")
            forwarded_for = request.headers.get("x-forwarded-for", "NOT SET")

            # Always log at INFO level so we can see what's happening
            if not has_header:
                request.META["HTTP_X_FORWARDED_PROTO"] = "https"
                log_msg = (
                    f"🔧 AzureProxyHeaderMiddleware: Set HTTP_X_FORWARDED_PROTO=https for {request.path} "
                    f"(REMOTE_ADDR={client_ip}, X-Forwarded-For={forwarded_for}, "
                    f"scheme={request_scheme}, is_secure={is_secure})"
                )
                logger.info(log_msg)
                print(log_msg, flush=True)
            else:
                log_msg = (
                    f"✅ AzureProxyHeaderMiddleware: Header already set for {request.path} "
                    f"(value={header_value}, REMOTE_ADDR={client_ip}, X-Forwarded-For={forwarded_for}, "
                    f"scheme={request_scheme}, is_secure={is_secure})"
                )
                logger.info(log_msg)
                print(log_msg, flush=True)
        except Exception as e:
            # Log any errors so we can see if middleware is failing
            error_msg = f"❌ AzureProxyHeaderMiddleware ERROR: {e}"
            logger.error(error_msg, exc_info=True)
            print(error_msg, flush=True)

        response = self.get_response(request)
        return response
