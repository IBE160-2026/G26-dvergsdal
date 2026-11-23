"""`send_answer` and the FR-74 answer states (Story 2.6a).

FR-41, FR-74, FR-75, AD-2, AD-3, AD-4, AD-9, NFR-2. Every service row of the
story's I/O matrix with `now` fixed: Sigmund's send, a switched respondent,
nobody coming, partial days, a re-send, the deadline (the last second of the
deadline day accepted, Oslo midnight refused), another household's ids, the
admin actor and a missing member, each refusal writing nothing. Then the
FR-74 states and the two models' fields (no total, no status). The views are
in test_rsvp_send.py.
"""

import datetime
from zoneinfo import ZoneInfo

import pytest

from wedding.actors import SYSTEM, AdminActor, GuestActor
from wedding.models import Guest, Household, HouseholdAnswer, PersonAnswer, Settings, User
from wedding.rules.answer import Answer
from wedding.rules.households import (
    COMING,
    NOT_ANSWERED,
    NOT_COMING,
    household_state,
    person_state,
)
from wedding.services.answers import send_answer
from wedding.services.exceptions import DeadlinePassed, InvalidAnswer, NotAllowed

SIGMUND = "test-sigmund0000000000"
ARILD = "test-arild000000000000"
OSLO = ZoneInfo("Europe/Oslo")
DEADLINE = datetime.date(2027, 6, 1)
# FR-41: the last second of the deadline day, and Oslo midnight after it.
LAST_SECOND = datetime.datetime(2027, 6, 1, 23, 59, 59, tzinfo=OSLO)
CLOSED = datetime.datetime(2027, 6, 2, 0, 0, tzinfo=OSLO)

NOTHING = {
    "coming": False,
    "friday": False,
    "saturday": False,
    "sunday": False,
    "cabin": False,
    "friday_dinner": False,
    "saturday_breakfast": False,
    "sunday_breakfast": False,
    "hike": "",
}

pytestmark = pytest.mark.django_db


@pytest.fixture
def deadline(seeded):
    Settings.objects.filter(pk=1).update(rsvp_deadline=DEADLINE)


def _actor(code: str) -> GuestActor:
    guest = Guest.objects.get(code=code)
    return GuestActor(guest=guest, household=guest.household)


def _ids(code: str) -> list[int]:
    household = Guest.objects.get(code=code).household
    return list(household.guests.order_by("id").values_list("id", flat=True))


def _sigmund_answer() -> Answer:
    """MT-36 b): both coming all weekend, both in the cabin, bestemor Sunday
    breakfast, hikes «Kanskje» and «Nei»."""
    sigmund, bestemor = _ids(SIGMUND)
    return Answer(
        {sigmund: True, bestemor: True},
        True,
        night={sigmund: True, bestemor: True},
        meals={bestemor: ["sunday_breakfast"]},
        hike={sigmund: "maybe", bestemor: "no"},
    )


def _row(guest_id: int) -> dict:
    row = PersonAnswer.objects.get(guest_id=guest_id)
    return {field: getattr(row, field) for field in NOTHING}


def _counts() -> tuple[int, int, int]:
    return (
        HouseholdAnswer.objects.count(),
        PersonAnswer.objects.count(),
        sum(Household.objects.values_list("revision", flat=True)),
    )


def _send(actor, code, respondent, answer, now=LAST_SECOND, household=None):
    household = household or Guest.objects.get(code=code).household
    return send_answer(actor, household=household, respondent=respondent, answer=answer, now=now)


def test_sigmund_sends(deadline):
    """FR-74, AD-4, AD-9 (matrix «Sigmund sends»): one HouseholdAnswer sent by
    Sigmund at `now`, two PersonAnswer rows, revision 0 to 1."""
    sigmund, bestemor = _ids(SIGMUND)
    sent = _send(_actor(SIGMUND), SIGMUND, sigmund, _sigmund_answer())
    assert (sent.sent_by_id, sent.sent_by_name, sent.sent_at) == (sigmund, "Sigmund", LAST_SECOND)
    assert HouseholdAnswer.objects.count() == 1
    assert PersonAnswer.objects.count() == 2
    everything = dict.fromkeys(("coming", "friday", "saturday", "sunday", "cabin"), True)
    assert _row(sigmund) == NOTHING | everything | {"hike": "maybe"}
    assert _row(bestemor) == NOTHING | everything | {"sunday_breakfast": True, "hike": "no"}
    assert Guest.objects.get(code=SIGMUND).household.revision == 1


def test_the_switched_respondent_is_the_sender(deadline):
    """FR-12, FR-74 (matrix «Bytt»): bestemor as respondent is recorded as the sender."""
    _, bestemor = _ids(SIGMUND)
    sent = _send(_actor(SIGMUND), SIGMUND, bestemor, _sigmund_answer())
    assert (sent.sent_by_id, sent.sent_by_name) == (bestemor, "bestemor")


def test_nobody_coming(deadline):
    """FR-75 (matrix «Nobody coming»): both rows `coming=False`, everything else
    False or blank, even with stray choices in the answer."""
    sigmund, bestemor = _ids(SIGMUND)
    answer = Answer(
        {sigmund: False, bestemor: False},
        True,
        night={sigmund: True},
        meals={sigmund: ["friday_dinner"]},
        hike={sigmund: "yes"},
    )
    _send(_actor(SIGMUND), SIGMUND, sigmund, answer)
    assert _row(sigmund) == NOTHING
    assert _row(bestemor) == NOTHING


def test_partial_days(deadline):
    """FR-14, FR-17, FR-75 (matrix «Partial days»): Filippa only Saturday, no hike;
    Leone not coming has everything False."""
    arild, marie, filippa, leone = _ids(ARILD)
    answer = Answer(
        {arild: True, marie: True, filippa: True, leone: False},
        False,
        days={arild: ["fri", "sat", "sun"], marie: ["fri", "sat", "sun"], filippa: ["sat"]},
        night={arild: False, marie: False, filippa: False},
        hike={arild: "yes", marie: "no", filippa: "yes"},
    )
    _send(_actor(ARILD), ARILD, marie, answer)
    assert _row(filippa) == NOTHING | {"coming": True, "saturday": True}
    assert _row(leone) == NOTHING
    assert _row(arild)["hike"] == "yes"
    assert HouseholdAnswer.objects.get().sent_by_name == "Marie"


def test_a_re_send_updates_the_rows(deadline):
    """AD-9 (matrix «Re-send»): the second send updates the same rows (one
    HouseholdAnswer, one PersonAnswer per guest) with the new sender and time,
    and the revision rises by exactly one more."""
    sigmund, bestemor = _ids(SIGMUND)
    earlier = LAST_SECOND - datetime.timedelta(hours=1)
    first = _send(_actor(SIGMUND), SIGMUND, sigmund, _sigmund_answer(), now=earlier)
    rows = dict(PersonAnswer.objects.values_list("guest_id", "pk"))
    assert Guest.objects.get(code=SIGMUND).household.revision == 1
    _send(_actor(SIGMUND), SIGMUND, bestemor, Answer({sigmund: True, bestemor: False}, True))
    sent = HouseholdAnswer.objects.get()
    assert sent.pk == first.pk
    assert (sent.sent_by_id, sent.sent_by_name, sent.sent_at) == (bestemor, "bestemor", LAST_SECOND)
    assert dict(PersonAnswer.objects.values_list("guest_id", "pk")) == rows
    assert _row(bestemor) == NOTHING
    assert _row(sigmund)["cabin"] is False
    assert Guest.objects.get(code=SIGMUND).household.revision == 2


def test_after_the_deadline_nothing_is_written(deadline):
    """FR-41, AD-11 (matrix «After deadline»): from Oslo midnight after the
    deadline day a guest send raises `DeadlinePassed` and writes nothing."""
    sigmund, _ = _ids(SIGMUND)
    before = _counts()
    with pytest.raises(DeadlinePassed) as refused:
        _send(_actor(SIGMUND), SIGMUND, sigmund, _sigmund_answer(), now=CLOSED)
    assert refused.value.message == "Svarfristen har gått ut."
    assert _counts() == before


def test_the_system_actor_is_not_bound_by_the_deadline(deadline):
    """FR-41, AD-3: the seed command (Story 2.6d) sends whatever the deadline is."""
    sigmund, _ = _ids(SIGMUND)
    _send(SYSTEM, SIGMUND, sigmund, _sigmund_answer(), now=CLOSED)
    assert HouseholdAnswer.objects.count() == 1


def test_another_household_is_refused(deadline):
    """AD-3, AD-6 (matrix «Other household»): a guest actor cannot write to another
    household, nor name another household's guest in its own answer."""
    sigmund, bestemor = _ids(SIGMUND)
    arild = _ids(ARILD)[0]
    before = _counts()
    attempts = [
        (_actor(ARILD), sigmund, _sigmund_answer()),
        (_actor(SIGMUND), arild, _sigmund_answer()),
        (_actor(SIGMUND), sigmund, Answer({sigmund: True, bestemor: True, arild: True}, True)),
        (
            _actor(SIGMUND),
            sigmund,
            Answer({sigmund: True, bestemor: True}, True, hike={arild: "yes"}),
        ),
    ]
    for actor, respondent, answer in attempts:
        with pytest.raises(NotAllowed):
            _send(actor, SIGMUND, respondent, answer)
    assert _counts() == before


def test_an_admin_actor_is_refused(deadline):
    """AD-10 (matrix «Admin actor»): the couple's override is Story 4.4."""
    sigmund, _ = _ids(SIGMUND)
    couple = User.objects.create(username="par-test", role=User.Role.COUPLE)
    with pytest.raises(NotAllowed):
        _send(AdminActor(couple), SIGMUND, sigmund, _sigmund_answer())
    assert HouseholdAnswer.objects.count() == 0


def test_a_missing_member_is_refused(deadline):
    """FR-74, AD-9: every guest of the household needs an attendance entry."""
    sigmund, _ = _ids(SIGMUND)
    before = _counts()
    with pytest.raises(InvalidAnswer) as refused:
        _send(_actor(SIGMUND), SIGMUND, sigmund, Answer({sigmund: True}, True))
    assert refused.value.message == "Svaret ble ikke sendt."
    assert _counts() == before


@pytest.mark.parametrize(
    ("coming", "state"), [(True, COMING), (False, NOT_COMING), (None, NOT_ANSWERED)]
)
def test_person_state(coming, state):
    """FR-74, AD-2: a person's state from their «Kommer»."""
    assert person_state(coming) == state


@pytest.mark.parametrize(
    ("answered", "coming", "state"),
    [
        (False, [], NOT_ANSWERED),
        (False, [True], NOT_ANSWERED),
        (True, [True, False], COMING),
        (True, [False, True], COMING),
        (True, [False, False], NOT_COMING),
        (True, [], NOT_COMING),
    ],
)
def test_household_state(answered, coming, state):
    """FR-74, AD-2: not answered until sent; then coming when anyone comes."""
    assert household_state(answered, coming) == state


def test_the_models_store_no_derived_values():
    """AD-4, FR-74: the two models hold facts only, no total and no status."""
    household_fields = {field.name for field in HouseholdAnswer._meta.get_fields()}
    person_fields = {field.name for field in PersonAnswer._meta.get_fields()}
    assert household_fields == {"id", "household", "sent_by", "sent_by_name", "sent_at"}
    assert person_fields == {"id", "guest", *NOTHING}
    choices = PersonAnswer._meta.get_field("hike").choices
    assert choices == [("yes", "Ja"), ("no", "Nei"), ("maybe", "Kanskje")]
