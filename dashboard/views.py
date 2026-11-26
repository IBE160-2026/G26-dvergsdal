"""The admin views: login, logout and Oversikt (Story 3.1; FR-46, NFR-4, AD-10, AD-13).

The session cookie is scoped to `/admin/` and lasts 20 hours since the last
request (config/settings.py). The browser drops the cookie when it expires, so
the server cannot tell «logged out by time» from «never logged in». Login
therefore also sets the small `admin_seen` cookie, which holds no data; a login
page opened without a session but with that cookie says «Du ble logget ut fordi
du var borte en stund.» once, and the cookie is then deleted. Logout deletes it
too, so a deliberate logout shows no such text.
"""

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST, require_safe

from dashboard.access import admin_actor, admin_required, safe_next
from dashboard.forms import AdminLoginForm
from dashboard.navigation import nav_items

SEEN_COOKIE = "admin_seen"
SEEN_COOKIE_AGE = 30 * 24 * 60 * 60
EXPIRED_TEXT = "Du ble logget ut fordi du var borte en stund."


class AdminLoginView(LoginView):
    """FR-46, NFR-4, AD-13: the login page at `/admin/logg-inn/` (UX A1: error and expired)."""

    template_name = "dashboard/login.html"
    authentication_form = AdminLoginForm
    redirect_authenticated_user = True

    def get_redirect_url(self) -> str:
        """NFR-4: `next` only when it is a path under `/admin/`; anything else is dropped."""
        target = self.request.POST.get("next", self.request.GET.get("next", ""))
        return safe_next(self.request, target)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """AD-13: an unauthenticated visitor with the marker cookie sees the expired notice once."""
        seen = (
            request.method == "GET"
            and SEEN_COOKIE in request.COOKIES
            and not request.user.is_authenticated
        )
        self.expired = seen
        response = super().get(request, *args, **kwargs)
        if seen:
            response.delete_cookie(SEEN_COOKIE, path=settings.SESSION_COOKIE_PATH)
        return response

    def form_valid(self, form: AdminLoginForm) -> HttpResponse:
        """AD-13: log in, then set the marker cookie that tells a later visit about an expiry."""
        response = super().form_valid(form)
        response.set_cookie(
            SEEN_COOKIE,
            "1",
            max_age=SEEN_COOKIE_AGE,
            path=settings.SESSION_COOKIE_PATH,
            secure=settings.SESSION_COOKIE_SECURE,
            httponly=True,
            samesite="Lax",
        )
        return response

    def get_context_data(self, **kwargs) -> dict[str, object]:
        """UX A1: the messages to show as notices, and whether this is the expired state."""
        context = super().get_context_data(**kwargs)
        form = context["form"]
        problems = []
        if form.is_bound:
            problems = list(form.non_field_errors()) + [
                message for field in form for message in field.errors
            ]
        context["problems"] = problems
        context["expired"] = getattr(self, "expired", False) and not problems
        context["expired_text"] = EXPIRED_TEXT
        return context


login_view = never_cache(AdminLoginView.as_view())


@never_cache
@require_POST
def logout_view(request: HttpRequest) -> HttpResponse:
    """FR-46, AD-13: «Logg ut» flushes the session, so the login page shows no expired notice."""
    logout(request)
    response = redirect("dashboard:login")
    response.delete_cookie(SEEN_COOKIE, path=settings.SESSION_COOKIE_PATH)
    return response


@admin_required
@require_safe
def home(request: HttpRequest) -> HttpResponse:
    """FR-46, UX A2 (Story 3.1: the frame only): Oversikt, with the panels to come in 3.2."""
    actor = admin_actor(request)
    return render(
        request,
        "dashboard/home.html",
        {"username": actor.user.get_username(), "nav_items": nav_items("home")},
    )


@admin_required
def unknown(request: HttpRequest, rest: str) -> HttpResponse:
    """UX-DR36: an admin address that is not a page gives the couple's own 404 (never G1)."""
    raise Http404
