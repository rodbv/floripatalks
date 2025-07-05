from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import PermissionDenied


class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        # Always allow the signup page to render
        return True

    def save_user(self, request, user, form, commit=True):
        # Block local signup attempts (form POSTs)
        sociallogin = getattr(request, "sociallogin", None)
        if sociallogin is None:
            raise PermissionDenied("Signup is only allowed via Google.")
        # Set is_staff for specific user
        if user.email == "rodrigo.vieira@gmail.com":
            user.is_staff = True
        return super().save_user(request, user, form, commit=commit)
