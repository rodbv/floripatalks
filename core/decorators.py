"""
Decorators for views.
"""

from collections.abc import Callable
from functools import wraps
from urllib.parse import urlparse

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django_htmx.http import HttpResponseClientRedirect


def require_authentication(view_func: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    """
    Decorator that requires user authentication.

    Works with both regular requests and HTMX requests:
    - Regular requests: Standard Django redirect to login
    - HTMX requests: Uses HttpResponseClientRedirect for full page redirect

    Usage:
        @require_authentication
        def my_view(request):
            ...
    """
    # Use Django's login_required as base
    decorated_view = login_required(view_func)

    @wraps(view_func)
    def wrapper(request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse:
        if not request.user.is_authenticated:
            login_url = reverse("account_login")

            # For HTMX requests, use the referrer (the page the user was viewing)
            # instead of the HTMX endpoint URL (e.g., /vote/) to redirect back to the host page
            if request.htmx:
                referrer = request.headers.get("referer")
                if referrer:
                    # Extract path from referrer (in case it's a full URL)
                    parsed = urlparse(referrer)
                    next_url = parsed.path
                    if parsed.query:
                        next_url += f"?{parsed.query}"
                else:
                    # Fallback to current path if no referrer
                    next_url = request.get_full_path()
            else:
                # For regular requests, use the current path
                next_url = request.get_full_path()

            redirect_url = f"{login_url}?next={next_url}"

            # For HTMX requests, use HttpResponseClientRedirect for full page redirect
            if request.htmx:
                return HttpResponseClientRedirect(redirect_url)

            # For regular requests, use standard redirect
            return redirect(redirect_url)

        # User is authenticated, call the original view
        return decorated_view(request, *args, **kwargs)

    return wrapper
