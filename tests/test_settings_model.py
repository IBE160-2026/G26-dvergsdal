"""The single-row `Settings` and the tables Story 1.2 adds (FR-3, FR-64, AD-4, AD-9).

The data migration creates the one row, so a fresh database already has settings
and guest views never need to create them. The check constraint refuses a second
row, and the data migration can be reversed and applied again.
"""

import datetime
import importlib

import pytest
from django.core.management import call_command
from django.db import IntegrityError, migrations, transaction

from wedding.models import Household, Settings

SCHEMA_MIGRATION = "0002_household_guest_settings"


@pytest.mark.django_db
def test_migrate_creates_exactly_one_settings_row_with_placeholders():
    """FR-3, FR-64: after `migrate` the one row exists, with safe placeholders."""
    assert Settings.objects.count() == 1
    settings_row = Settings.objects.get()
    assert settings_row.pk == 1
    assert (settings_row.contact_1_name, settings_row.contact_2_name) == ("Rikke", "Valdemar")
    assert (settings_row.contact_1_phone, settings_row.contact_2_phone) == ("", "")
    assert (settings_row.vipps_number, settings_row.account_number) == ("", "")
    prices = [
        settings_row.price_cabin_weekend,
        settings_row.price_friday_dinner,
        settings_row.price_saturday_breakfast,
        settings_row.price_sunday_breakfast,
    ]
    assert prices == [0, 0, 0, 0]
    assert all(type(price) is int for price in prices)  # AD-12: whole kroner
    assert settings_row.rsvp_deadline == datetime.date(2028, 1, 4)


@pytest.mark.django_db
def test_a_second_settings_row_is_refused():
    """FR-64, AD-4: settings are a single row; the check constraint refuses pk 2."""
    row = Settings.objects.get()
    row.pk = None
    with pytest.raises(IntegrityError), transaction.atomic():
        row.save()
    assert Settings.objects.count() == 1


@pytest.mark.django_db
def test_a_new_household_starts_at_revision_0():
    """AD-9: `Household.revision` is 0 for a new household."""
    assert Household().revision == 0


def test_the_schema_migration_adds_only_household_guest_and_settings():
    """Story 1.2 AC: 0002 creates `Household`, `Guest` and `Settings` and no other table."""
    schema = importlib.import_module(f"wedding.migrations.{SCHEMA_MIGRATION}").Migration
    created = {op.name for op in schema.operations if isinstance(op, migrations.CreateModel)}
    assert created == {"Household", "Guest", "Settings"}
    assert all(isinstance(op, migrations.CreateModel) for op in schema.operations)


@pytest.mark.django_db(transaction=True, serialized_rollback=True)
def test_the_settings_data_migration_reverses_and_reapplies():
    """Story 1.2 AC: reversing the data migration deletes the row, and reapplying recreates it.

    `serialized_rollback` restores the migrated row before the test, so it starts
    from the same state as a fresh `migrate`.
    """
    assert Settings.objects.count() == 1

    call_command("migrate", "wedding", SCHEMA_MIGRATION, verbosity=0)
    assert Settings.objects.count() == 0

    call_command("migrate", "wedding", verbosity=0)
    assert Settings.objects.count() == 1
