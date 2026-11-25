"""The `seed_testdata` command, the reset service and the conflict check (Story 1.3).

Covers every row of the Story 1.3 I/O matrix: first run, second run, a taken code,
a taken username and a wrong `APP_ENV` (FR-68, FR-72, AD-14, AD-16). The
"Settings, helper" row is in `test_settings_service.py`. Story 2.6d adds the
answers, allergies and consents the seed sends, the totals against expected.toml,
a bad `consent_by`, a missing or unreadable seed.toml and the printed labels.
"""

import datetime
import tomllib
import uuid
from io import StringIO
from pathlib import Path

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone

from wedding import selectors
from wedding.actors import SYSTEM, AdminActor
from wedding.management.commands.seed_testdata import seed_answer
from wedding.models import (
    Allergy,
    Consent,
    Guest,
    Household,
    HouseholdAnswer,
    PersonAnswer,
    Settings,
    Submission,
    User,
)
from wedding.rules.allergies import AllergyEntry
from wedding.rules.answer import Answer
from wedding.rules.money import household_total
from wedding.selectors import form_prices
from wedding.services.answers import send_answer
from wedding.services.consent import CONSENT_TEXT_VERSION
from wedding.services.exceptions import NotAllowed
from wedding.services.households import NewGuest, create_household
from wedding.services.testdata import reset_test_data

SEED_FILE = Path(__file__).resolve().parent.parent / "wedding" / "fixtures" / "seed.toml"
SEED = tomllib.loads(SEED_FILE.read_text(encoding="utf-8"))
SEED_GUESTS = [guest for household in SEED["households"] for guest in household["guests"]]
SIGMUNDS_CODE = SEED_GUESTS[0]["code"]
EXPECTED = tomllib.loads((SEED_FILE.parent / "expected.toml").read_text(encoding="utf-8"))
ANSWERED = [household for household in SEED["households"] if "answered_by" in household]
DAY_FIELDS = {"fri": "friday", "sat": "saturday", "sun": "sunday"}
MEAL_FIELDS = ("friday_dinner", "saturday_breakfast", "sunday_breakfast")


def seed():
    """Run the command and return what it printed."""
    out = StringIO()
    call_command("seed_testdata", stdout=out)
    return out.getvalue()


def make_couple(username="rikke"):
    return AdminActor(User.objects.create_user(username=username, role=User.Role.COUPLE))


def snapshot():
    """Everything the command could write, to show that a refusal wrote nothing."""
    return (
        list(Household.objects.values_list("id", "is_test_data")),
        list(Guest.objects.values_list("id", "name", "code")),
        list(User.objects.values_list("id", "username", "is_test_data")),
        list(Settings.objects.values()),
        HouseholdAnswer.objects.count(),
        Submission.objects.count(),
        Consent.objects.count(),
    )


# The examiner's machine: no APP_ENV set (NFR-8); `local_env` is in conftest.py.
pytestmark = pytest.mark.usefixtures("local_env")


# First run


@pytest.mark.django_db
def test_first_run_creates_the_seed_households_and_guests_as_test_data():
    """FR-68, AD-16: 7 households and 14 guests with the names, contacts and codes in seed.toml."""
    seed()

    assert Household.objects.count() == len(SEED["households"]) == 7
    assert not Household.objects.filter(is_test_data=False).exists()
    stored = [
        [(g.name, g.phone, g.email, g.code) for g in household.guests.all()]
        for household in Household.objects.prefetch_related("guests")
    ]
    planned = [
        [
            (g["name"], g.get("phone", ""), g.get("email", ""), g["code"])
            for g in household["guests"]
        ]
        for household in SEED["households"]
    ]
    assert stored == planned
    assert Guest.objects.count() == 14


@pytest.mark.django_db
def test_first_run_sets_the_settings_with_the_deadline_30_days_from_today():
    """FR-68, AD-16: fictional prices and contacts, and a deadline that keeps the form open."""
    seed()

    row = Settings.objects.get()
    planned = SEED["settings"]
    for name in [
        "contact_1_name",
        "contact_1_phone",
        "contact_2_name",
        "contact_2_phone",
        "price_cabin_weekend",
        "price_friday_dinner",
        "price_saturday_breakfast",
        "price_sunday_breakfast",
        "vipps_number",
        "account_number",
    ]:
        assert getattr(row, name) == planned[name], name
    assert row.rsvp_deadline == timezone.localdate() + datetime.timedelta(days=30)


@pytest.mark.django_db
def test_first_run_creates_a_test_couple_and_a_test_helper():
    """FR-47, FR-68: `testpar` and `testhjelper`, with the password from seed.toml."""
    seed()

    users = {user.username: user for user in User.objects.all()}
    assert set(users) == {"testpar", "testhjelper"}
    assert users["testpar"].role == User.Role.COUPLE
    assert users["testhjelper"].role == User.Role.HELPER
    for user in users.values():
        assert user.is_test_data
        assert user.check_password("bryllup-test-2028")


@pytest.mark.django_db
def test_first_run_prints_a_test_link_per_guest_and_both_logins():
    """FR-68: the examiner can copy each guest's link and the logins from the output."""
    printed = seed()

    for guest in SEED_GUESTS:
        line = next(line for line in printed.splitlines() if f"/{guest['code']}/" in line)
        assert guest["name"] in line
        assert f"http://127.0.0.1:8000/{guest['code']}/" in line
    assert "testpar / bryllup-test-2028" in printed
    assert "testhjelper / bryllup-test-2028" in printed


# Second run


@pytest.mark.django_db
def test_a_second_run_gives_the_same_result_and_leaves_the_couples_household_alone():
    """FR-72, AD-16: the old test data is replaced; data the seed did not make is kept."""
    first = seed()
    couple = make_couple()
    kept = create_household(couple, [NewGuest("Kari"), NewGuest("Ola")])
    kept_guests = list(kept.guests.values_list("id", "name", "code"))

    second = seed()

    assert second == first
    assert Household.objects.filter(is_test_data=True).count() == 7
    assert Guest.objects.filter(household__is_test_data=True).count() == 14
    assert list(Household.objects.filter(is_test_data=False)) == [kept]
    assert list(kept.guests.values_list("id", "name", "code")) == kept_guests
    assert set(User.objects.values_list("username", flat=True)) == {
        "rikke",
        "testpar",
        "testhjelper",
    }
    assert User.objects.get(username="rikke").is_test_data is False


# Conflicts with data the seed did not make


@pytest.mark.django_db
def test_a_seed_code_held_by_a_real_guest_stops_the_command_and_writes_nothing():
    """FR-72, AD-16: matrix row "Code taken": a CommandError names the code."""
    household = create_household(make_couple(), [NewGuest("Kari")])
    household.guests.update(code=SIGMUNDS_CODE)  # as if a real guest had this code
    before = snapshot()

    with pytest.raises(CommandError) as refused:
        seed()

    assert SIGMUNDS_CODE in str(refused.value)
    assert "Ingenting ble endret." in str(refused.value)
    assert snapshot() == before


@pytest.mark.django_db
def test_a_seed_username_held_by_a_real_user_stops_the_command_and_writes_nothing():
    """FR-72, AD-16: matrix row "Username taken": a CommandError names the user."""
    User.objects.create_user(username="testpar", role=User.Role.COUPLE)
    before = snapshot()

    with pytest.raises(CommandError) as refused:
        seed()

    assert "«testpar»" in str(refused.value)
    assert "testhjelper" not in str(refused.value)
    assert snapshot() == before


@pytest.mark.django_db
def test_a_conflict_after_an_earlier_run_keeps_the_earlier_test_data():
    """FR-72: a refusal on a later run does not reset either, since nothing is written."""
    seed()
    Household.objects.filter(is_test_data=True).update(is_test_data=False)  # now "real" data
    before = snapshot()

    with pytest.raises(CommandError) as refused:
        seed()

    assert SIGMUNDS_CODE in str(refused.value)
    assert snapshot() == before


@pytest.mark.django_db
def test_a_value_a_service_refuses_undoes_the_reset_too(monkeypatch, tmp_path):
    """FR-72, AD-3: a refusal after the reset has run rolls everything back, reset included."""
    seed()
    before = snapshot()
    broken = tmp_path / "seed.toml"
    broken.write_text(
        SEED_FILE.read_text(encoding="utf-8").replace(
            "price_cabin_weekend = 1500", "price_cabin_weekend = -1"
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("wedding.management.commands.seed_testdata.SEED_PATH", broken)

    with pytest.raises(CommandError) as refused:
        seed()

    assert "Prisen for hytte kan ikke være negativ." in str(refused.value)
    assert "Ingenting ble endret." in str(refused.value)
    assert snapshot() == before


# APP_ENV


@pytest.mark.django_db
@pytest.mark.parametrize("app_env", ["production", "prod", "Local", "local "])
def test_any_app_env_but_local_is_refused_and_nothing_is_written(monkeypatch, app_env):
    """FR-72, AD-14: matrix row "Wrong env": an allow list, so a misspelling never passes."""
    monkeypatch.setenv("APP_ENV", app_env)
    before = snapshot()

    with pytest.raises(CommandError) as refused:
        seed()

    message = str(refused.value)
    assert f"APP_ENV er «{app_env}»" in message
    assert "«local»" in message
    assert snapshot() == before


@pytest.mark.django_db
@pytest.mark.parametrize("app_env", ["local", ""])
def test_app_env_local_or_empty_is_allowed(monkeypatch, app_env):
    """AD-14, NFR-8: `local`, and empty as unset, are the examiner's machine."""
    monkeypatch.setenv("APP_ENV", app_env)

    seed()

    assert Household.objects.count() == 7


@pytest.mark.django_db
def test_production_settings_are_refused_even_without_app_env_in_the_environment(settings):
    """AD-14: the command also checks the loaded settings, not only the variable."""
    settings.APP_ENV = "production"

    with pytest.raises(CommandError) as refused:
        seed()

    assert "APP_ENV er «production»" in str(refused.value)
    assert Household.objects.count() == 0


# The reset service


@pytest.mark.django_db
def test_reset_removes_only_test_households_guests_and_users():
    """FR-72, AD-4, AD-16: rows the couple made are never touched."""
    create_household(SYSTEM, [NewGuest("Sigmund"), NewGuest("bestemor")])
    couple = make_couple()
    kept = create_household(couple, [NewGuest("Kari")])
    User.objects.create_user(username="testpar", is_test_data=True)

    reset_test_data(SYSTEM)

    assert list(Household.objects.all()) == [kept]
    assert list(Guest.objects.values_list("name", flat=True)) == ["Kari"]
    assert list(User.objects.all()) == [couple.user]


@pytest.mark.django_db
@pytest.mark.parametrize("role", [User.Role.COUPLE, User.Role.HELPER])
def test_only_the_system_actor_may_reset(role):
    """AD-3, AD-16: admins cannot remove test data; only the seed command does."""
    create_household(SYSTEM, [NewGuest("Sigmund")])
    actor = AdminActor(User.objects.create_user(username="rikke", role=role))

    with pytest.raises(NotAllowed):
        reset_test_data(actor)

    assert Household.objects.count() == 1


# The conflict check


@pytest.mark.django_db
def test_conflicts_name_only_codes_and_usernames_used_by_real_data():
    """FR-72, AD-16: test rows are not conflicts, since the reset replaces them."""
    create_household(SYSTEM, [NewGuest("Sigmund", code="test-sigmund0000000000")])
    real = create_household(make_couple(), [NewGuest("Kari")])
    real.guests.update(code="test-bestemor000000000")
    User.objects.create_user(username="testhjelper", is_test_data=True)

    conflicts = selectors.seed_conflicts(
        ["test-sigmund0000000000", "test-bestemor000000000", "test-eva00000000000000"],
        ["testpar", "testhjelper", "rikke"],
    )

    assert conflicts == ["lenkekoden «test-bestemor000000000»", "brukernavnet «rikke»"]


# Story 2.6d: answers, allergies and consents


def household_of(seed_household):
    return Household.objects.get(guests__code=seed_household["guests"][0]["code"])


@pytest.mark.django_db
def test_first_run_sends_an_answer_for_every_household_but_mona():
    """FR-68, AD-3, AD-16, AD-20: matrix row "First run"; Mona's household stays at 0."""
    seed()

    assert HouseholdAnswer.objects.count() == 6
    assert Submission.objects.filter(kind=Submission.ANSWER).count() == 6
    mona = Guest.objects.get(name="Mona").household
    for household in Household.objects.all():
        assert household.revision == (0 if household == mona else 1)
    assert not PersonAnswer.objects.filter(guest__household=mona).exists()
    assert PersonAnswer.objects.count() == 12


@pytest.mark.django_db
def test_each_guests_stored_answer_matches_seed_toml():
    """FR-13 to FR-17, FR-68, FR-74: coming, days, cabin, meals, hike and the sender."""
    seed()

    for planned_household in ANSWERED:
        sender = next(
            g for g in planned_household["guests"] if g["key"] == planned_household["answered_by"]
        )
        assert household_of(planned_household).answer.sent_by_name == sender["name"]
        for planned in planned_household["guests"]:
            row = PersonAnswer.objects.get(guest__code=planned["code"])
            key = planned["key"]
            assert row.coming == planned["coming"], key
            for day, name in DAY_FIELDS.items():
                assert getattr(row, name) == (day in planned.get("days", [])), key
            assert row.cabin == planned.get("overnight", False), key
            for meal in MEAL_FIELDS:
                assert getattr(row, meal) == (meal in planned.get("meals", [])), key
            assert row.hike == planned.get("hike", ""), key


@pytest.mark.django_db
def test_allergies_are_stored_only_for_guests_who_said_yes():
    """FR-25, FR-26, FR-68, AD-18: matrix row "Allergies"."""
    seed()

    stored = {a.guest.name: a for a in Allergy.objects.select_related("guest")}
    assert set(stored) == {"Sigmund", "bestemor", "Arild", "Eva", "Jonas", "Synne"}
    for name in ("Sigmund", "Arild", "Jonas"):
        assert stored[name].none, name
    assert stored["bestemor"].gluten
    assert stored["Eva"].shellfish
    assert stored["Eva"].other
    assert stored["Eva"].note == "Tåler ikke koriander."
    assert stored["Synne"].nuts


@pytest.mark.django_db
def test_consents_are_given_or_refused_by_the_respondent():
    """FR-26, FR-27, FR-29, FR-68, AD-18: matrix row "Consents"."""
    seed()

    events = {c.guest.name: c for c in Consent.objects.select_related("guest", "given_by")}
    given = {"Sigmund", "bestemor", "Arild", "Eva", "Jonas", "Synne"}
    assert set(events) == given | {"Filippa", "Ida"}
    for name in given:
        assert events[name].event == Consent.GIVEN, name
    assert events["Filippa"].event == events["Ida"].event == Consent.REFUSED
    assert events["bestemor"].given_by.name == "Sigmund"
    assert events["Filippa"].given_by.name == "Arild"
    assert events["Ida"].given_by.name == "Jonas"
    assert {c.text_version for c in events.values()} == {CONSENT_TEXT_VERSION}


@pytest.mark.django_db
def test_each_answered_households_total_equals_expected_toml():
    """FR-33, FR-69, AD-12: matrix row "Totals", worked out from the stored answers."""
    seed()
    prices = form_prices()

    for planned_household in ANSWERED:
        rows = PersonAnswer.objects.filter(guest__household=household_of(planned_household))
        stored = Answer(
            attendance={row.guest_id: row.coming for row in rows},
            whole=False,
            days={
                row.guest_id: tuple(day for day, name in DAY_FIELDS.items() if getattr(row, name))
                for row in rows
            },
            night={row.guest_id: row.cabin for row in rows if row.coming},
            meals={
                row.guest_id: tuple(meal for meal in MEAL_FIELDS if getattr(row, meal))
                for row in rows
            },
        )
        key = planned_household["key"]
        assert household_total(stored, prices) == EXPECTED["households"][key]["total"], key


@pytest.mark.django_db
def test_a_second_run_keeps_a_real_answer_and_its_submission():
    """FR-72, AD-4, AD-20: matrix row "Second run"; only the test submissions are replaced."""
    first = seed()
    kept = create_household(make_couple(), [NewGuest("Kari"), NewGuest("Ola")])
    kari, ola = kept.guests.all()
    real = send_answer(
        SYSTEM,
        household=kept,
        respondent=kari.pk,
        answer=Answer(attendance={kari.pk: False, ola.pk: False}, whole=None),
        now=timezone.now(),
        submission=uuid.uuid4(),
        revision=0,
        shown_total=0,
        consent_version=None,
    )
    real_submission = Submission.objects.get(object_id=real.pk)

    second = seed()

    assert second == first
    assert HouseholdAnswer.objects.get(household=kept) == real
    assert Submission.objects.get(pk=real_submission.pk).object_id == real.pk
    test_submissions = Submission.objects.exclude(pk=real_submission.pk)
    assert test_submissions.count() == 6
    for submission in test_submissions:
        assert HouseholdAnswer.objects.filter(
            pk=submission.object_id, household__is_test_data=True
        ).exists()


@pytest.mark.django_db
def test_print_labels_the_roles_and_says_the_settings_were_replaced():
    """FR-47, FR-68, AD-16: the role labels and the settings line in the printout."""
    lines = seed().splitlines()

    assert "Innstillingene er erstattet med testverdiene fra seed.toml." in lines
    assert any("testpar /" in line and "(brudeparet)" in line for line in lines)
    assert any("testhjelper /" in line and "(hjelper)" in line for line in lines)


@pytest.mark.django_db
def test_a_consent_by_other_than_the_respondent_stops_the_command(monkeypatch, tmp_path):
    """FR-29, AD-16: matrix row "Bad consent_by": the guest key is named, nothing written."""
    broken = tmp_path / "seed.toml"
    broken.write_text(
        SEED_FILE.read_text(encoding="utf-8").replace(
            'allergy_categories = ["gluten"]\nconsent = "yes"\nconsent_by = "sigmund"',
            'allergy_categories = ["gluten"]\nconsent = "yes"\nconsent_by = "arild"',
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("wedding.management.commands.seed_testdata.SEED_PATH", broken)
    before = snapshot()

    with pytest.raises(CommandError) as refused:
        seed()

    assert "«bestemor»" in str(refused.value)
    assert snapshot() == before


@pytest.mark.django_db
@pytest.mark.parametrize("content", [None, "not = toml ="])
def test_a_missing_or_unreadable_seed_toml_stops_the_command(monkeypatch, tmp_path, content):
    """AD-16: matrix row "Missing / invalid seed.toml": nothing is written."""
    path = tmp_path / "seed.toml"
    if content is not None:
        path.write_text(content, encoding="utf-8")
    monkeypatch.setattr("wedding.management.commands.seed_testdata.SEED_PATH", path)
    before = snapshot()

    with pytest.raises(CommandError) as refused:
        seed()

    assert str(refused.value).startswith("Fant ikke eller kunne ikke lese")
    assert snapshot() == before


# The mapping from a seed household to an Answer


def test_seed_answer_is_the_whole_weekend_when_everyone_coming_comes_all_days():
    """FR-14, FR-68, AD-2: `whole` True and no days; a guest not coming is left out."""
    planned = {
        "answered_by": "a",
        "guests": [
            {
                "key": "a",
                "coming": True,
                "days": ["fri", "sat", "sun"],
                "overnight": True,
                "meals": [],
                "hike": "yes",
                "no_allergies": True,
                "consent": "yes",
                "consent_by": "a",
            },
            {"key": "b", "coming": False},
        ],
    }

    respondent, answer = seed_answer(planned, {"a": 1, "b": 2})

    assert respondent == 1
    assert answer.whole is True
    assert answer.days == {}
    assert answer.attendance == {1: True, 2: False}
    assert answer.hike == {1: "yes"}
    assert answer.allergies == {1: AllergyEntry(none=True)}
    assert answer.consent == {1: True}
    assert answer.confirmed == frozenset()


def test_seed_answer_sets_days_and_confirms_a_consent_given_for_someone_else():
    """FR-14, FR-27, FR-68, AD-2: `whole` False with days for all; no consent is no entry."""
    planned = {
        "answered_by": "a",
        "guests": [
            {
                "key": "a",
                "coming": True,
                "days": ["fri", "sat", "sun"],
                "overnight": False,
                "meals": ["friday_dinner"],
            },
            {
                "key": "b",
                "coming": True,
                "days": ["sat"],
                "overnight": False,
                "meals": [],
                "allergy_categories": ["nuts"],
                "allergy_note": "x",
                "consent": "yes",
                "consent_by": "a",
            },
            {
                "key": "c",
                "coming": True,
                "days": ["sat", "sun"],
                "overnight": True,
                "meals": [],
                "consent": "no",
            },
        ],
    }

    _, answer = seed_answer(planned, {"a": 1, "b": 2, "c": 3})

    assert answer.whole is False
    assert answer.days == {1: ("fri", "sat", "sun"), 2: ("sat",), 3: ("sat", "sun")}
    assert answer.consent == {2: True, 3: False}
    assert answer.confirmed == frozenset({2})
    assert answer.allergies[2] == AllergyEntry(cats=("nuts",), note="x")
    assert answer.hike == {}
