"""All models of the wedding website; this app owns the data.

Story 1.1 adds only the custom `User`, so that it is `AUTH_USER_MODEL` from the
very first migration (AD-10). Households, guests and settings follow in Story 1.2.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """An admin account for the couple or a helper (AD-10, FR-46, FR-47).

    Guests are never users: they come in only through their personal link (AD-6).
    A new account is a helper unless made a couple account, so a mistake gives
    the least privilege.
    """

    class Role(models.TextChoices):
        COUPLE = "couple", "Brudepar"
        HELPER = "helper", "Hjelper"

    role = models.CharField("rolle", max_length=10, choices=Role, default=Role.HELPER)
