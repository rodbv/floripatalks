from django.shortcuts import render

# Create your views here.


def home(request):
    """Simple home page view"""
    context = {
        "user": request.user,
        "is_authenticated": request.user.is_authenticated,
    }
    return render(request, "core/home.html", context)
