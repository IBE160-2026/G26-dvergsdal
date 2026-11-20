"""All models of the wedding website; this app owns the data (AD-1).

Story 1.1 added the custom `User`, so that it is `AUTH_USER_MODEL` from the very
first migration (AD-10). Story 1.2 adds households, guests and the single-row
settings. Story 1.3 marks the households and users the seed command creates as
test data (FR-72, AD-16). Each later table comes with the story that needs it.

Only `wedding/services/` writes these models (AD-3), and only facts are stored,
never derived values such as totals or a household's display name (AD-4).
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

PHONE_MAX_LENGTH = 30


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
    # FR-72, AD-16: made by the seed command; only these are removed by the reset.
    is_test_data = models.BooleanField("testdata", default=False)


class Household(models.Model):
    """The people invited together, who answer together (FR-49, AD-4).

    No name is stored: «for Sigmund og bestemor» is derived from the guests' names
    by `wedding.rules.households.household_names` (Story 1.5). `revision` starts
    at 0 and goes up on every change to the household's answer or members, so
    two senders never overwrite silently (AD-9).
    """

    revision = models.PositiveIntegerField("revisjon", default=0)
    # FR-72, AD-16: made by the seed command; only these are removed by the reset.
    is_test_data = models.BooleanField("testdata", default=False)

    class Meta:
        ordering = ("id",)
        verbose_name = "husstand"
        verbose_name_plural = "husstander"

    def __str__(self):
        return f"Husstand {self.pk}"


class Guest(models.Model):
    """One invited person and their personal link code (FR-1, FR-2, FR-49, AD-6).

    The code is the guest's only login: 22 URL-safe characters from
    `wedding.links.new_code()`, unique (and so indexed) and with no personal data.
    """

    household = models.ForeignKey(
        Household, on_delete=models.CASCADE, related_name="guests", verbose_name="husstand"
    )
    name = models.CharField("navn", max_length=100)
    phone = models.CharField("telefon", max_length=PHONE_MAX_LENGTH, blank=True)
    email = models.EmailField("e-post", blank=True)
    # 22 is `wedding.links.CODE_LENGTH`; a test keeps the two equal.
    code = models.CharField("lenkekode", max_length=22, unique=True)

    class Meta:
        ordering = ("id",)
        verbose_name = "gjest"
        verbose_name_plural = "gjester"

    def __str__(self):
        return self.name


class Settings(models.Model):
    """The one row of settings: contacts, prices, deadline and payment details.

    FR-6 (contact numbers on every guest page), FR-32 (prices in whole kroner,
    AD-12), FR-41 (the deadline as a date, AD-11) and FR-64 (Vipps and account
    number). A data migration creates the row; guest views read it with `.get()`
    and never create it (FR-3). The check constraint refuses a second row.
    """

    contact_1_name = models.CharField("kontaktperson 1", max_length=100)
    contact_1_phone = models.CharField(
        "telefon kontaktperson 1", max_length=PHONE_MAX_LENGTH, blank=True
    )
    contact_2_name = models.CharField("kontaktperson 2", max_length=100)
    contact_2_phone = models.CharField(
        "telefon kontaktperson 2", max_length=PHONE_MAX_LENGTH, blank=True
    )
    price_cabin_weekend = models.PositiveIntegerField("pris for hytte hele helgen (kr)")
    price_friday_dinner = models.PositiveIntegerField("pris for middag fredag (kr)")
    price_saturday_breakfast = models.PositiveIntegerField("pris for frokost lørdag (kr)")
    price_sunday_breakfast = models.PositiveIntegerField("pris for frokost søndag (kr)")
    rsvp_deadline = models.DateField("svarfrist")
    vipps_number = models.CharField("Vipps-nummer", max_length=20, blank=True)
    account_number = models.CharField("kontonummer", max_length=20, blank=True)

    class Meta:
        constraints = (
            models.CheckConstraint(condition=models.Q(pk=1), name="wedding_settings_single_row"),
        )
        verbose_name = "innstillinger"
        verbose_name_plural = "innstillinger"

    def __str__(self):
        return "Innstillinger"
