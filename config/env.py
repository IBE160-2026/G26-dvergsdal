"""Read settings from environment variables, with safe local defaults (AD-14, NFR-8).

Everything here is a plain function of its arguments, so each case of the
production guard is an ordinary unit test. `config/settings.py` collects the
values and raises; these helpers only parse and judge them. Messages are in
Norwegian because they are what a person sees when the app refuses to start.
"""

from collections.abc import Mapping

from django.core.exceptions import ImproperlyConfigured

APP_ENVS = ("local", "production")
DEFAULT_APP_ENV = "local"

# Safe only on a developer's own machine; production refuses to start with it.
LOCAL_SECRET_KEY = "django-insecure-local-only-never-use-in-production"
LOCAL_ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]

_TRUE = {"1", "true", "yes", "on"}
_FALSE = {"0", "false", "no", "off"}


def _read(environ: Mapping[str, str], name: str) -> str | None:
    """Return the variable's value, treating unset, empty and blank alike as None."""
    value = environ.get(name)
    if value is None or not value.strip():
        return None
    return value


def validate_app_env(value: str | None) -> str:
    """Return the app environment, refusing anything outside the allow list (AD-14).

    Unset or empty means `local`, so the examiner needs no `.env` (NFR-8). Any
    other value must match exactly: `prod` or `Production` on a server must never
    fall back to local defaults with DEBUG on.
    """
    if value is None or not value.strip():
        return DEFAULT_APP_ENV
    if value not in APP_ENVS:
        allowed = " eller ".join(f"«{env}»" for env in APP_ENVS)
        raise ImproperlyConfigured(f"APP_ENV er «{value}», men må være {allowed}.")
    return value


def read_bool(environ: Mapping[str, str], name: str, *, default: bool) -> bool:
    """Read a true/false variable such as DEBUG; unset or empty gives `default`."""
    value = _read(environ, name)
    if value is None:
        return default
    normalised = value.strip().lower()
    if normalised in _TRUE:
        return True
    if normalised in _FALSE:
        return False
    raise ImproperlyConfigured(f"{name} er «{value}», men må være «true» eller «false».")


def read_str(environ: Mapping[str, str], name: str, *, default: str) -> str:
    """Read a text variable such as SECRET_KEY; unset or empty gives `default`."""
    value = _read(environ, name)
    return default if value is None else value


def read_list(environ: Mapping[str, str], name: str, *, default: list[str]) -> list[str]:
    """Read a comma-separated variable such as ALLOWED_HOSTS; unset or empty gives `default`."""
    value = _read(environ, name)
    if value is None:
        return list(default)
    return [item.strip() for item in value.split(",") if item.strip()]


def production_problems(debug: bool, secret_key: str, allowed_hosts: list[str]) -> list[str]:
    """List every reason the app must not start with `APP_ENV=production` (AD-14, NFR-4).

    An empty list means production settings are safe to start with. All problems
    are returned together so one restart is enough to see what to fix.
    """
    problems = []
    if debug:
        problems.append("DEBUG er slått på. Sett DEBUG=false.")
    if not secret_key.strip() or secret_key == LOCAL_SECRET_KEY:
        problems.append(
            "SECRET_KEY mangler eller er den lokale standardnøkkelen. "
            "Sett en lang, tilfeldig nøkkel."
        )
    if not allowed_hosts:
        problems.append("ALLOWED_HOSTS er tom. Sett domenet nettsiden skal svare på.")
    return problems


def refusal_message(problems: list[str]) -> str:
    """Join the production problems into the one message shown when startup is refused."""
    lines = "\n".join(f"- {problem}" for problem in problems)
    return f"Appen starter ikke med APP_ENV=production:\n{lines}"
