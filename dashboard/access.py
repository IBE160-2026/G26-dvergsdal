"""Who may open an admin page (FR-46, NFR-4, AD-10, AD-13).

Access is `request.user` authenticated, active and with a valid role. Anything
else is sent to the login page with `?next=` set to the page asked for, and
every admin response says `Cache-Control: no-store` (`never_cache`), so a shared
or back-forward cache never keeps the couple's page. `admin_actor` is the only
way a view makes an `AdminActor`.
"""

from collections.abc import Callable
from functools import wraps
from urllib.parse import unquote, urlsplit

from django.contrib.auth.views import redirect_to_login
from django.http import HttpRequest, HttpResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache

from wedding.actors import AdminActor
from wedding.models import User

ADMIN_PREFIX = "/admin/"
LOGIN_PATHS = {"/admin/logg-inn", "/admin/logg-ut"}


def is_admin(user) -> bool:
    """FR-46, AD-10: an authenticated, active user with the role of the couple or a helper."""
    return bool(user.is_authenticated and user.is_active and user.role in User.Role.values)


def admin_actor(request: HttpRequest) -> AdminActor:
    """AD-3, AD-10: the actor for a request that `admin_required` has let through."""
    return AdminActor(request.user)


def admin_required(view: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    """FR-46, AD-10, AD-13: redirect to the login page unless the visitor is an admin."""

    @wraps(view)
    def wrapper(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not is_admin(request.user):
            return redirect_to_login(request.get_full_path(), login_url="dashboard:login")
        return view(request, *args, **kwargs)

    return never_cache(wrapper)


def safe_next(request: HttpRequest, target: str) -> str:
    """NFR-4: `target` when it is a path on this site under `/admin/`, else an empty string.

    A link code or another site never becomes the place a login leads to. Dot
    segments are refused, since `/admin/../<code>/` would leave `/admin/` once a
    browser tidies it.
    """
    if not url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}):
        return ""
    parts = urlsplit(target)
    if parts.scheme or parts.netloc or not parts.path.startswith(ADMIN_PREFIX):
        return ""
    path = unquote(parts.path)
    if {".", ".."} & set(path.split("/")):
        return ""
    if path.rstrip("/") in LOGIN_PATHS:
        return ""  # a login that leads back to the login or logout page would loop
    return target
