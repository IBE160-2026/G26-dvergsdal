"""All models of the wedding website; this app owns the data (AD-1).

Story 1.1 added the custom `User`, so that it is `AUTH_USER_MODEL` from the very
first migration (AD-10). Story 1.2 adds households, guests and the single-row
settings. Story 1.3 marks the households and users the seed command creates as
test data (FR-72, AD-16). Story 3.1 adds a check constraint on `User.role` (AD-10).
Story 2.6a adds a household's sent answer,
`HouseholdAnswer` and one `PersonAnswer` per guest (FR-74, AD-4). Story 2.6b
adds each guest's `Allergy` and the append-only `Consent` events (FR-26, FR-29,
AD-18). Story 2.6c adds `Submission`, the one-time submission ids already
written (AD-20, NFR-1). Each later
table comes with the story that needs it.

Only `wedding/services/` writes these models (AD-3), and only facts are stored,
never derived values such as totals or a household's display name (AD-4).
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

from wedding.rules.allergies import NOTE_MAX
from wedding.rules.days import HIKE_ANSWERS, HIKE_LABELS

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

    class Meta(AbstractUser.Meta):
        # AD-10 (Story 3.1): the role is always couple or helper, also when a row is
        # written outside a form, so no account has a blank or unknown role.
        constraints = (
            models.CheckConstraint(
                condition=models.Q(role__in=["couple", "helper"]), name="user_role_valid"
            ),
        )


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


class HouseholdAnswer(models.Model):
    """A household's sent answer: who sent it and when (Story 2.6a, FR-74, AD-4, AD-9).

    Written only by `wedding.services.answers.send_answer`. `sent_by_name`
    keeps the sender's name as text, so it stays if the guest is removed.
    Nothing derived is stored: no total and no status.
    """

    household = models.OneToOneField(
        Household, on_delete=models.CASCADE, related_name="answer", verbose_name="husstand"
    )
    sent_by = models.ForeignKey(
        Guest,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
        verbose_name="sendt av",
    )
    sent_by_name = models.CharField("sendt av (navn)", max_length=100)
    sent_at = models.DateTimeField("sendt")

    class Meta:
        verbose_name = "svar fra husstand"
        verbose_name_plural = "svar fra husstander"

    def __str__(self):
        return f"Svar fra husstand {self.household_id}"


class PersonAnswer(models.Model):
    """One guest's sent answer (Story 2.6a, FR-13 to FR-17, FR-74, AD-4).

    The normalised answer as facts: coming, the days, the cabin, the paid
    meals and the Friday hike (blank when not asked). Someone not coming has
    every other field False or blank.
    """

    guest = models.OneToOneField(
        Guest, on_delete=models.CASCADE, related_name="answer", verbose_name="gjest"
    )
    coming = models.BooleanField("kommer")
    friday = models.BooleanField("fredag", default=False)
    saturday = models.BooleanField("lørdag", default=False)
    sunday = models.BooleanField("søndag", default=False)
    cabin = models.BooleanField("overnatting i hytte", default=False)
    friday_dinner = models.BooleanField("middag fredag", default=False)
    saturday_breakfast = models.BooleanField("frokost lørdag", default=False)
    sunday_breakfast = models.BooleanField("frokost søndag", default=False)
    hike = models.CharField(
        "fjelltur fredag",
        max_length=5,
        blank=True,
        choices=[(key, HIKE_LABELS[key]) for key in HIKE_ANSWERS],
    )

    class Meta:
        ordering = ("guest_id",)
        verbose_name = "svar fra gjest"
        verbose_name_plural = "svar fra gjester"

    def __str__(self):
        return f"Svar fra gjest {self.guest_id}"


class Allergy(models.Model):
    """A guest's current allergy data, kept only with their «Ja» to consent.

    Story 2.6b, FR-25, FR-26, FR-29, AD-4, AD-18. One boolean per
    `ALLERGY_KEYS` category, «Ingen allergier eller matbehov» (`none`) and the
    note. Written only by `wedding.services.answers.send_answer`; deleted on
    «Nei» or when the guest stops coming. Nothing derived is stored.
    """

    guest = models.OneToOneField(
        Guest, on_delete=models.CASCADE, related_name="allergy", verbose_name="gjest"
    )
    gluten = models.BooleanField("gluten", default=False)
    lactose = models.BooleanField("laktose", default=False)
    nuts = models.BooleanField("nøtter", default=False)
    shellfish = models.BooleanField("skalldyr", default=False)
    vegetarian = models.BooleanField("vegetar", default=False)
    vegan = models.BooleanField("vegan", default=False)
    other = models.BooleanField("annet", default=False)
    none = models.BooleanField("ingen allergier eller matbehov", default=False)
    note = models.CharField("merknad", max_length=NOTE_MAX, blank=True)

    class Meta:
        ordering = ("guest_id",)
        verbose_name = "allergi"
        verbose_name_plural = "allergier"

    def __str__(self):
        return f"Allergi for gjest {self.guest_id}"


class Consent(models.Model):
    """One consent event for a guest's allergy data (Story 2.6b, FR-26, FR-29, AD-18).

    Append-only: given, refused or withdrawn (Story 7.2), when, by whom (the
    respondent guest, or a user for the couple's override in Story 4.4, and
    the name as text, kept if they are removed) and `CONSENT_TEXT_VERSION`.
    """

    GIVEN = "given"
    REFUSED = "refused"
    WITHDRAWN = "withdrawn"
    EVENTS = ((GIVEN, "gitt"), (REFUSED, "nektet"), (WITHDRAWN, "trukket tilbake"))

    guest = models.ForeignKey(
        Guest, on_delete=models.CASCADE, related_name="consents", verbose_name="gjest"
    )
    event = models.CharField("hendelse", max_length=10, choices=EVENTS)
    at = models.DateTimeField("tidspunkt")
    given_by = models.ForeignKey(
        Guest,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
        verbose_name="svart av gjest",
    )
    given_by_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
        verbose_name="svart av bruker",
    )
    given_by_name = models.CharField("svart av (navn)", max_length=100)
    text_version = models.CharField("versjon av samtykketeksten", max_length=20)

    class Meta:
        ordering = ("at", "pk")
        verbose_name = "samtykke"
        verbose_name_plural = "samtykker"

    def __str__(self):
        return f"Samtykke {self.pk}"


class Submission(models.Model):
    """A one-time submission id that has been written (Story 2.6c, AD-20, NFR-1).

    Every write form carries a fresh id; the service records it in the same
    transaction as the write, with what was written (`kind`, `object_id`). A
    second POST with the same id finds it and writes nothing, so a double tap
    or a resubmit never doubles an answer. A refused send records none.
    """

    ANSWER = "answer"
    KINDS = ((ANSWER, "svar"),)

    key = models.UUIDField("innsendings-id", unique=True)
    kind = models.CharField("type", max_length=20, choices=KINDS)
    object_id = models.PositiveBigIntegerField("id for det som ble lagret")
    created_at = models.DateTimeField("tidspunkt")

    class Meta:
        ordering = ("created_at", "pk")
        verbose_name = "innsending"
        verbose_name_plural = "innsendinger"

    def __str__(self):
        return f"Innsending {self.pk}"
