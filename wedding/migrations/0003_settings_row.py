"""Create the one `Settings` row with safe placeholders (Story 1.2, FR-3, FR-64).

A fresh `migrate` without test data already has settings, so guest views can read
them with `.get()` and never create them. Phones, Vipps and account number are
blank and prices are 0 until the couple fills them in (Story 4.5); the deadline
is EXPERIENCE.md's example date.
"""

import datetime

from django.db import migrations

SETTINGS_PK = 1


def create_settings_row(apps, schema_editor):
    Settings = apps.get_model("wedding", "Settings")
    Settings.objects.create(
        pk=SETTINGS_PK,
        contact_1_name="Rikke",
        contact_1_phone="",
        contact_2_name="Valdemar",
        contact_2_phone="",
        price_cabin_weekend=0,
        price_friday_dinner=0,
        price_saturday_breakfast=0,
        price_sunday_breakfast=0,
        rsvp_deadline=datetime.date(2028, 1, 4),
        vipps_number="",
        account_number="",
    )


def delete_settings_row(apps, schema_editor):
    Settings = apps.get_model("wedding", "Settings")
    Settings.objects.filter(pk=SETTINGS_PK).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("wedding", "0002_household_guest_settings"),
    ]

    operations = [
        migrations.RunPython(create_settings_row, delete_settings_row),
    ]
