"""Personal link codes and the one resolver that turns a code into a guest actor (AD-6).

A code is `secrets.token_urlsafe(16)`: 128 random bits as 22 URL-safe characters,
with no personal data (FR-1, NFR-4). `resolve_code` is the only way from a code to
a guest; every guest view uses it. It only reads, so opening a link never writes
(FR-3), and a code in the wrong format never reaches the database.
"""

import re
import secrets

from wedding.actors import GuestActor
from wedding.models import Guest

CODE_LENGTH = 22
CODE_BYTES = 16
_CODE_PATTERN = re.compile(rf"[A-Za-z0-9_-]{{{CODE_LENGTH}}}")


def is_code_format(code: object) -> bool:
    """AD-6: True when `code` has exactly 22 characters from `[A-Za-z0-9_-]`."""
    return isinstance(code, str) and _CODE_PATTERN.fullmatch(code) is not None


def new_code() -> str:
    """FR-1, AD-6: a fresh, unguessable code.

    A random 128-bit code collides with negligible probability, so there is no
    retry; the unique constraint on `Guest.code` is the backstop.
    """
    return secrets.token_urlsafe(CODE_BYTES)


def resolve_code(code: object) -> GuestActor | None:
    """FR-1, FR-2, FR-3, AD-6: the guest actor for a known code, else None.

    The format is checked before any query, and the lookup is one SELECT that
    also loads the household.
    """
    if not is_code_format(code):
        return None
    try:
        guest = Guest.objects.select_related("household").get(code=code)
    except Guest.DoesNotExist:
        return None
    return GuestActor(guest=guest, household=guest.household)
