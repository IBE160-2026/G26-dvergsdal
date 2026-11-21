"""Which steps the RSVP form has, and the step registry (Story 2.1).

FR-14, UX-DR19, AD-7: `form_steps` for step 1 not completed, someone coming
and nobody coming, over every household shape in seed.toml; `step_position`,
`next_step` and `previous_step`; and the registry's slugs and names in
wedding/rsvp/steps.py, with the addresses a mount builds.
"""

import tomllib
from pathlib import Path

import pytest

from wedding.rsvp.steps import CHECK, CHECK_SLUG, KEY_BY_SLUG, STEPS, FormMount
from wedding.rules.form_steps import (
    STEP_KEYS,
    form_steps,
    next_step,
    previous_step,
    step_position,
)

SEED_FILE = Path(__file__).resolve().parent.parent / "wedding" / "fixtures" / "seed.toml"
SEED = tomllib.loads(SEED_FILE.read_text(encoding="utf-8"))
ALL = ("who", "days", "overnight", "meals", "allergies", "hike")


def test_step_keys_are_in_the_form_order():
    """FR-14: who, days, overnight, meals, allergies, hike."""
    assert STEP_KEYS == ALL


@pytest.mark.parametrize(
    "household", SEED["households"], ids=[household["key"] for household in SEED["households"]]
)
def test_form_steps_over_every_seed_household(household):
    """FR-14, UX-DR19: before step 1 all six count; with the seeded answers, all six
    when anyone comes and only step 1 when nobody does; and every member alone
    coming or not coming."""
    size = len(household["guests"])
    attendance = [guest.get("coming") for guest in household["guests"]]
    assert form_steps(None) == ALL
    if None not in attendance:  # households that have not answered have no answers
        assert form_steps(attendance) == (ALL if any(attendance) else ("who",))
    assert form_steps([False] * size) == ("who",)
    for index in range(size):
        assert form_steps([position == index for position in range(size)]) == ALL


@pytest.mark.parametrize(
    ("steps", "key", "position", "after", "before"),
    [
        (ALL, "who", (1, 6), "days", None),
        (ALL, "days", (2, 6), "overnight", "who"),
        (ALL, "allergies", (5, 6), "hike", "meals"),
        (ALL, "hike", (6, 6), None, "allergies"),
        (("who",), "who", (1, 1), None, None),
    ],
)
def test_position_next_and_previous(steps, key, position, after, before):
    """UX-DR19, AD-7: «Steg n av m», the next step (None is the check page) and the
    previous one (None is before step 1)."""
    assert step_position(steps, key) == position
    assert next_step(steps, key) == after
    assert previous_step(steps, key) == before


@pytest.mark.parametrize("key", ALL[1:])
def test_a_step_that_does_not_apply_goes_on_to_the_check_page(key):
    """AD-7: with nobody coming, every later step's next applicable address is the
    check page, and the step before it is step 1."""
    assert next_step(("who",), key) is None
    assert previous_step(("who",), key) == "who"


def test_step_position_needs_an_applicable_step():
    """UX-DR19: a step that does not apply has no position."""
    with pytest.raises(ValueError, match=r"tuple.index"):
        step_position(("who",), "days")


def test_registry_has_every_step_with_its_slug_and_name():
    """AD-7, UX-DR19: one registry entry per step key, with the Norwegian slugs and
    the names the progress line shows; the check page is `se-over`."""
    assert tuple(STEPS) == STEP_KEYS
    assert {key: (step.slug, step.name) for key, step in STEPS.items()} == {
        "who": ("", "Hvem kommer"),
        "days": ("dager", "Dager"),
        "overnight": ("overnatting", "Overnatting"),
        "meals": ("maltider", "Måltider"),
        "allergies": ("allergier", "Allergier og matbehov"),
        "hike": ("fjelltur", "Fjelltur fredag"),
    }
    assert CHECK_SLUG == "se-over"
    assert KEY_BY_SLUG == {
        "dager": "days",
        "overnatting": "overnight",
        "maltider": "meals",
        "allergier": "allergies",
        "fjelltur": "hike",
        "se-over": CHECK,
    }


def test_mount_builds_every_address():
    """AD-7: step 1 at the base address, the others under it, the check page at
    `se-over/`; None is the check page too."""
    mount = FormMount(base_path="/abc/svar/", cookie_path="/abc/", exit_url="/abc/#svar")
    assert mount.url("who") == "/abc/svar/"
    assert mount.url("days") == "/abc/svar/dager/"
    assert mount.url("hike") == "/abc/svar/fjelltur/"
    assert mount.url(CHECK) == "/abc/svar/se-over/"
    assert mount.url(None) == "/abc/svar/se-over/"
