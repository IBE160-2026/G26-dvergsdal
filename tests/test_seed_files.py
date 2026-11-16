"""The two data files: `seed.toml` and the hand-worked `expected.toml` (FR-68, FR-69, NFR-3).

These tests check the files themselves, without a database: the seed data is
fictional (NFR-3), every FR-68 case is present, the codes are valid, and
`expected.toml` has an entry for every household and guest with values from the
allowed sets. They never compute the expected numbers; the stories that build the
rules assert those (AD-16).
"""

import re
import tomllib
from pathlib import Path

import pytest

from wedding.links import CODE_LENGTH, is_code_format
from wedding.models import User
from wedding.rules.households import MAX_HOUSEHOLD_SIZE, MIN_HOUSEHOLD_SIZE

FIXTURES = Path(__file__).resolve().parent.parent / "wedding" / "fixtures"


def load(name):
    with (FIXTURES / name).open("rb") as file:
        return tomllib.load(file)


SEED = load("seed.toml")
EXPECTED = load("expected.toml")
HOUSEHOLDS = SEED["households"]
GUESTS = [guest for household in HOUSEHOLDS for guest in household["guests"]]

# NFR-3: "+47 000" is no Norwegian subscriber number; 1xx keeps them apart.
IMPOSSIBLE_PHONE = re.compile(r"\+47 000 00 1\d\d")
REAL_PEOPLE = {"Rikke", "Valdemar"}
ALLERGY_CATEGORIES = {"gluten", "lactose", "nuts", "shellfish", "vegetarian", "vegan", "other"}
PAYMENT_STATUSES = {"paid", "part_paid", "not_paid", "nothing_to_pay", "refund_owed"}


def mod11_is_valid(account_number: str) -> bool:
    """The check digit rule for Norwegian account numbers (11 digits, weights 5432765432)."""
    digits = [int(char) for char in account_number if char.isdigit()]
    if len(digits) != 11:
        return False
    weighted = sum(d * w for d, w in zip(digits[:10], [5, 4, 3, 2, 7, 6, 5, 4, 3, 2], strict=True))
    check = (11 - weighted % 11) % 11
    return check != 10 and check == digits[10]


def test_mod11_helper_accepts_a_valid_number_and_rejects_a_changed_one():
    """NFR-3: the helper below is itself right, so «fails MOD11» means something."""
    assert mod11_is_valid("1234.56.78903")  # check digit 3 is the valid one
    assert not mod11_is_valid("1234.56.78904")


# NFR-3: only fictional people and contact details


def test_every_email_is_on_example_com():
    """NFR-3: no email in the seed data can reach a real person."""
    emails = [guest["email"] for guest in GUESTS if "email" in guest]
    assert emails
    assert all(email.endswith("@example.com") for email in emails)


def test_every_phone_number_is_impossible():
    """NFR-3: every guest phone and both contact phones are `+47 000 00 1xx`."""
    phones = [guest["phone"] for guest in GUESTS if "phone" in guest]
    phones += [SEED["settings"]["contact_1_phone"], SEED["settings"]["contact_2_phone"]]
    assert all(IMPOSSIBLE_PHONE.fullmatch(phone) for phone in phones), phones


def test_the_payment_details_cannot_receive_money():
    """FR-68, NFR-3: Vipps `00000` and an account number that fails MOD11."""
    assert SEED["settings"]["vipps_number"] == "00000"
    assert not mod11_is_valid(SEED["settings"]["account_number"])


def test_only_rikke_and_valdemar_are_real():
    """NFR-3: the couple are the contacts, and no guest shares their names."""
    contacts = {SEED["settings"]["contact_1_name"], SEED["settings"]["contact_2_name"]}
    assert contacts == REAL_PEOPLE
    assert not {guest["name"] for guest in GUESTS} & REAL_PEOPLE


# Settings and users


def test_the_fictional_prices_and_deadline():
    """FR-68, AD-12: 2026-level prices in whole kroner and a deadline 30 days ahead."""
    settings = SEED["settings"]
    prices = [
        settings["price_cabin_weekend"],
        settings["price_friday_dinner"],
        settings["price_saturday_breakfast"],
        settings["price_sunday_breakfast"],
    ]
    assert prices == [1500, 340, 260, 260]
    assert settings["deadline_days_from_today"] == 30


def test_a_test_couple_and_a_test_helper():
    """FR-47, FR-68: `testpar` (couple) and `testhjelper` (helper)."""
    users = {(user["username"], user["role"], user["password"]) for user in SEED["users"]}
    assert users == {
        ("testpar", User.Role.COUPLE, "bryllup-test-2028"),
        ("testhjelper", User.Role.HELPER, "bryllup-test-2028"),
    }


# Households, guests and codes


def test_keys_are_unique():
    """FR-69: households and guests are looked up by key in expected.toml."""
    household_keys = [household["key"] for household in HOUSEHOLDS]
    guest_keys = [guest["key"] for guest in GUESTS]
    assert len(set(household_keys)) == len(household_keys)
    assert len(set(guest_keys)) == len(guest_keys)


@pytest.mark.parametrize("household", HOUSEHOLDS, ids=lambda household: household["key"])
def test_no_household_is_larger_than_8(household):
    """FR-49, AD-8: every seed household has 1 to 8 people."""
    assert MIN_HOUSEHOLD_SIZE <= len(household["guests"]) <= MAX_HOUSEHOLD_SIZE


def test_codes_are_valid_unique_and_named_after_the_guest():
    """AD-6: fixed codes `test-<key>` padded with 0 to 22 characters."""
    codes = [guest["code"] for guest in GUESTS]
    assert all(is_code_format(code) for code in codes)
    assert len(set(codes)) == len(codes)
    for guest in GUESTS:
        assert guest["code"] == f"test-{guest['key']}".ljust(CODE_LENGTH, "0")


def test_the_people_from_uj_1_to_uj_3_are_there():
    """FR-68: Sigmund and bestemor; Arild, Marie, Filippa and Leone; Synne."""
    names = {guest["name"] for guest in GUESTS}
    assert {"Sigmund", "bestemor", "Arild", "Marie", "Filippa", "Leone", "Synne"} <= names


def test_answers_are_sent_by_someone_in_the_household():
    """FR-68: `answered_by` and `consent_by` name a guest in the same household."""
    for household in HOUSEHOLDS:
        keys = {guest["key"] for guest in household["guests"]}
        if "answered_by" in household:
            assert household["answered_by"] in keys
        for guest in household["guests"]:
            if "consent_by" in guest:
                assert guest["consent_by"] in keys


def test_planned_answers_use_the_allowed_values():
    """FR-14, FR-17, FR-25, FR-73: days, meals, hike and allergies are known values."""
    meals = {"friday_dinner", "saturday_breakfast", "sunday_breakfast"}
    day_patterns = [
        ["fri", "sat", "sun"],
        ["fri", "sat"],
        ["sat", "sun"],
        ["fri"],
        ["sat"],
        ["sun"],
    ]
    for guest in GUESTS:
        if guest.get("coming"):
            assert guest["days"] in day_patterns, guest["key"]
            assert set(guest["meals"]) <= meals, guest["key"]
            assert guest.get("hike", "yes") in {"yes", "no", "maybe"}
            assert ("hike" in guest) == ("fri" in guest["days"]), guest["key"]
        assert set(guest.get("allergy_categories", [])) <= ALLERGY_CATEGORIES
        assert guest.get("consent", "yes") in {"yes", "no"}


# Every FR-68 case


def _household(key):
    return next(household for household in HOUSEHOLDS if household["key"] == key)


def _guests_where(predicate):
    return [guest["key"] for guest in GUESTS if predicate(guest)]


def test_every_fr_68_case_is_present():
    """FR-68: the seed covers every case the expected-results list needs."""
    declines = [
        household["key"]
        for household in HOUSEHOLDS
        if "answered_by" in household and not any(guest["coming"] for guest in household["guests"])
    ]
    assert declines, "a household that declines entirely"
    assert _guests_where(lambda g: g.get("days") == ["sat"] and g.get("overnight") is False), (
        "a guest who comes only on Saturday, without a cabin"
    )
    statuses = {household["payment_status"] for household in EXPECTED["households"].values()}
    assert {"paid", "part_paid", "refund_owed"} <= statuses, "paid, part paid and refund owed"
    assert any(
        "payment_report" in household
        and EXPECTED["households"][household["key"]].get("report_matches") is False
        and not household.get("payments")
        for household in HOUSEHOLDS
    ), "an «I have paid» report with no matching payment"
    assert [h["key"] for h in HOUSEHOLDS if "answered_by" not in h], "a household not answered"
    assert _guests_where(
        lambda g: (
            g.get("allergy_categories")
            and g.get("consent") == "yes"
            and not g.get("consent_withdrawn")
        )
    ), "an allergy with consent"
    assert _guests_where(lambda g: g.get("allergy_categories") and g.get("consent") == "no"), (
        "an allergy without consent"
    )
    assert _guests_where(lambda g: g.get("consent_withdrawn")), "a withdrawn consent"


def test_a_household_that_has_not_answered_has_no_answer_fields():
    """FR-68: Mona and Geir have only names, contacts and codes."""
    for household in HOUSEHOLDS:
        if "answered_by" not in household:
            for guest in household["guests"]:
                assert set(guest) <= {"key", "name", "phone", "email", "code"}


# expected.toml matches seed.toml


def test_expected_has_exactly_the_seed_households_and_guests():
    """FR-69: every seed household and guest has one entry, and nothing else does."""
    assert set(EXPECTED["households"]) == {household["key"] for household in HOUSEHOLDS}
    assert set(EXPECTED["guests"]) == {guest["key"] for guest in GUESTS}


@pytest.mark.parametrize("key", sorted(EXPECTED["households"]))
def test_each_expected_household_uses_the_allowed_values(key):
    """FR-33, FR-60, FR-61: whole-kroner amounts and a known payment status."""
    expected = EXPECTED["households"][key]
    assert expected["payment_status"] in PAYMENT_STATUSES | {"not_answered"}
    for name in ("total", "received", "missing", "refund"):
        if name in expected:
            assert type(expected[name]) is int
            assert expected[name] >= 0
    assert ("missing" in expected) == (expected["payment_status"] == "part_paid")
    assert ("refund" in expected) == (expected["payment_status"] == "refund_owed")
    assert ("report_matches" in expected) == ("payment_report" in _household(key))
    assert (expected["payment_status"] == "not_answered") == ("answered_by" not in _household(key))


@pytest.mark.parametrize("key", sorted(EXPECTED["guests"]))
def test_each_expected_guest_uses_the_allowed_values(key):
    """FR-74, AD-18: a status, and an allergy state only for those coming."""
    expected = EXPECTED["guests"][key]
    assert expected["status"] in {"coming", "not_coming", "not_answered"}
    if expected["status"] == "coming":
        assert expected["allergy_state"] in {"has_allergies", "no_allergies", "nothing_stored"}
    else:
        assert "allergy_state" not in expected


def test_expected_counts_are_whole_numbers_from_zero():
    """FR-54: every count is a non-negative integer, and every category and status is listed."""
    counts = EXPECTED["counts"]
    for group in counts.values():
        for value in group.values():
            assert type(value) is int
            assert value >= 0
    assert set(counts["allergy_categories"]) == ALLERGY_CATEGORIES
    assert set(counts["allergy_states"]) == {"has_allergies", "no_allergies", "nothing_stored"}
    assert set(counts["hike"]) == {"yes", "maybe", "no"}
    assert set(counts["payment_status_coming"]) == PAYMENT_STATUSES
    assert {"saturday_lunch", "saturday_dinner"} <= set(counts["meals"])


def test_the_lock_cases_are_offsets_from_the_deadline():
    """FR-41, FR-42, AD-11: open the day before and at 23:59:59, locked from 00:00:00 after."""
    cases = [
        (case["days_after_deadline"], case["time"], case["locked"]) for case in EXPECTED["lock"]
    ]
    assert cases == [
        (-1, "12:00:00", False),
        (0, "23:59:59", False),
        (1, "00:00:00", True),
        (7, "12:00:00", True),
    ]
