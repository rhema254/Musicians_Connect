from django.contrib.auth.decorators import login_required, user_passes_test, REDIRECT_FIELD_NAME
from django.shortcuts import redirect
from functools import wraps


def client_required(func):
    @wraps(func)
    @login_required
    def decorated_view(request, *args, **kwargs):
        if not hasattr(request.user, "client"):
            return redirect("loginclients")  # Redirect to login if not a client
        return func(request, *args, **kwargs)
    return decorated_view


# def musician_required(func):
#     @wraps(func)
#     @login_required
#     def decorated_view(request, *args, **kwargs):
#         if not hasattr(request.user, "musician"):
#             return redirect("login")  # Redirect to login if not a client
#         return func(request, *args, **kwargs)
#     return decorated_view


def musician_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, 'musician'),
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# def apply_gig(request):
#     if request.method == "POST":
#         gig = request.POST.get("gig_id")
#         musician = request.POST.get("musician_id")
#         client = request.POST.get("client_id")
#         print(gig, musician, client)
#         return redirect("gigs")
#     return redirect("gigs")