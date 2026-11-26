"""The `send_answer` service and the FR-74 answer states (Stories 2.6a to 2.6c).

FR-26, FR-27, FR-29, FR-41, FR-74, FR-75, AD-2, AD-3, AD-4, AD-7, AD-9, AD-18,
AD-20, NFR-1, NFR-2, NFR-3. What the service does, by topic, with `now` fixed:
the send itself (the respondent, a switched respondent, nobody coming, partial
days, a re-send, the deadline: the last second of the deadline day accepted,
Oslo midnight refused); consent and allergy data (stored only with «Ja», for the
respondent and for another member, the `Allergy` and `Consent` fields, `str()`
and the log); a repeated or conflicting send (the submission id, two sends from
one revision, a changed total or consent text, the `Submission` model); and the
FR-74 states with the two models' fields (no total, no status). Every refusal
writes nothing. The views are in test_rsvp_send_views.py.
"""

import datetime
import logging
import uuid
from zoneinfo import ZoneInfo

import pytest
from django.db.models import F

from wedding.actors import SYSTEM, AdminActor, GuestActor
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
from wedding.rules.allergies import ALLERGY_KEYS, AllergyEntry
from wedding.rules.answer import Answer
from wedding.rules.households import (
    COMING,
    NOT_ANSWERED,
    NOT_COMING,
    household_state,
    person_state,
)
from wedding.rules.money import household_total
from wedding.selectors import form_prices, submitted
from wedding.services.answers import send_answer
from wedding.services.consent import CONSENT_TEXT_VERSION
from wedding.services.exceptions import (
    ConsentTextChanged,
    DeadlinePassed,
    InvalidAnswer,
    NotAllowed,
    RevisionConflict,
    TotalChanged,
)

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


def _send(actor, code, respondent, answer, now=LAST_SECOND, household=None, **story_2_6c):
    """`send_answer` with Story 2.6c's checks passing unless `story_2_6c`
    overrides them: a fresh submission id, the household's current revision,
    the total at today's prices and the current consent-text version."""
    household = household or Guest.objects.get(code=code).household
    checks = {
        "submission": uuid.uuid4(),
        "revision": Household.objects.get(pk=household.pk).revision,
        "shown_total": household_total(answer, form_prices()),
        "consent_version": CONSENT_TEXT_VERSION,
    } | story_2_6c
    return send_answer(
        actor, household=household, respondent=respondent, answer=answer, now=now, **checks
    )


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


# Story 2.6b: allergies and consent (FR-26, FR-27, FR-29, FR-75, AD-18, NFR-3).

GLUTEN = AllergyEntry(cats=("gluten",), note="Tåler litt")
LACTOSE = AllergyEntry(cats=("lactose",))
NUTS = AllergyEntry(cats=("nuts",))
NONE = AllergyEntry(none=True)
EARLIER = LAST_SECOND - datetime.timedelta(hours=1)


def _with(answer: Answer, allergies=None, consent=None, confirmed=()) -> Answer:
    return Answer(
        answer.attendance,
        answer.whole,
        days=answer.days,
        night=answer.night,
        meals=answer.meals,
        hike=answer.hike,
        allergies=allergies or {},
        consent=consent or {},
        confirmed=frozenset(confirmed),
    )


def _send_allergies(allergies=None, consent=None, confirmed=(), answer=None, now=LAST_SECOND):
    sigmund, _ = _ids(SIGMUND)
    answer = _with(answer or _sigmund_answer(), allergies, consent, confirmed)
    return _send(_actor(SIGMUND), SIGMUND, sigmund, answer, now=now)


def _member(who: str) -> int:
    return _ids(SIGMUND)[0 if who == "respondent" else 1]


def _allergy(guest_id: int) -> dict | None:
    row = Allergy.objects.filter(guest_id=guest_id).first()
    if row is None:
        return None
    cats = tuple(key for key in ALLERGY_KEYS if getattr(row, key))
    return {"cats": cats, "none": row.none, "note": row.note}


def _events(guest_id: int) -> list[str]:
    return list(Consent.objects.filter(guest_id=guest_id).values_list("event", flat=True))


def test_the_respondent_consents(deadline):
    """FR-26, FR-29, AD-18 (matrix «Respondent Ja»): Sigmund's data and a
    `given` event by him, at `now`, with the text version."""
    sigmund, _ = _ids(SIGMUND)
    _send_allergies({sigmund: GLUTEN}, {sigmund: True})
    assert _allergy(sigmund) == {"cats": ("gluten",), "none": False, "note": "Tåler litt"}
    consent = Consent.objects.get()
    assert (consent.guest_id, consent.event, consent.at) == (sigmund, Consent.GIVEN, LAST_SECOND)
    assert (consent.given_by_id, consent.given_by_name) == (sigmund, "Sigmund")
    assert consent.given_by_user is None
    assert consent.text_version == CONSENT_TEXT_VERSION == "2026-11-23"


def test_another_member_consents_when_confirmed(deadline):
    """FR-27, AD-18 (matrix «Other member Ja, confirmed»): stored, given by Sigmund."""
    sigmund, bestemor = _ids(SIGMUND)
    _send_allergies({bestemor: LACTOSE}, {bestemor: True}, confirmed=[bestemor])
    assert _allergy(bestemor) == {"cats": ("lactose",), "none": False, "note": ""}
    consent = Consent.objects.get()
    assert (consent.guest_id, consent.given_by_id, consent.given_by_name) == (
        bestemor,
        sigmund,
        "Sigmund",
    )


@pytest.mark.parametrize(
    "entry", [LACTOSE, AllergyEntry(cats=("gluten",), none=True)], ids=["unconfirmed", "conflict"]
)
def test_a_problem_writes_nothing(deadline, entry):
    """FR-25, FR-27, AD-3 (matrix «Other member Ja, not confirmed»): the service
    refuses an unconfirmed «Ja» for someone else, or «Ingen …» with a category,
    before any write."""
    _, bestemor = _ids(SIGMUND)
    before = _counts()
    with pytest.raises(InvalidAnswer):
        _send_allergies({bestemor: entry}, {bestemor: True})
    assert _counts() == before
    assert (Allergy.objects.count(), Consent.objects.count()) == (0, 0)


@pytest.mark.parametrize("who", ["respondent", "other"])
def test_nei_on_a_first_send(deadline, who):
    """FR-26, AD-18 (matrix «Nei, first send»): no data, one `refused` event."""
    guest_id = _member(who)
    _send_allergies({guest_id: NUTS}, {guest_id: False})
    assert _allergy(guest_id) is None
    assert _events(guest_id) == [Consent.REFUSED]


@pytest.mark.parametrize("who", ["respondent", "other"])
def test_unanswered_on_a_first_send(deadline, who):
    """FR-28, AD-18 (matrix «Unanswered, first send»): no data, no event."""
    guest_id = _member(who)
    _send_allergies({guest_id: NUTS})
    assert (Allergy.objects.count(), Consent.objects.count()) == (0, 0)


def test_none_is_stored_with_ja_only(deadline):
    """FR-25, FR-26 (matrix «Ingen … with Ja», «… with Nei / unanswered»)."""
    sigmund, bestemor = _ids(SIGMUND)
    _send_allergies({sigmund: NONE, bestemor: NONE}, {sigmund: True, bestemor: False})
    assert _allergy(sigmund) == {"cats": (), "none": True, "note": ""}
    assert _allergy(bestemor) is None
    _send_allergies({sigmund: NONE, bestemor: NONE}, {sigmund: True})
    assert _allergy(bestemor) is None


def test_ja_with_nothing_entered_deletes(deadline):
    """AD-18 (matrix «Ja, nothing entered»): the stored row goes, the event is kept."""
    sigmund, _ = _ids(SIGMUND)
    _send_allergies({sigmund: GLUTEN}, {sigmund: True}, now=EARLIER)
    _send_allergies(consent={sigmund: True})
    assert _allergy(sigmund) is None
    assert _events(sigmund) == [Consent.GIVEN, Consent.GIVEN]


@pytest.mark.parametrize("who", ["respondent", "other"])
def test_a_re_send_unanswered_keeps_the_data(deadline, who):
    """FR-28, AD-18 (matrix «Re-send, unanswered»): unchanged, no new event."""
    guest_id = _member(who)
    _send_allergies({guest_id: GLUTEN}, {guest_id: True}, confirmed=[guest_id], now=EARLIER)
    _send_allergies({guest_id: LACTOSE})
    assert _allergy(guest_id) == {"cats": ("gluten",), "none": False, "note": "Tåler litt"}
    assert _events(guest_id) == [Consent.GIVEN]


@pytest.mark.parametrize("who", ["respondent", "other"])
def test_a_re_send_nei_deletes_the_data(deadline, who):
    """FR-26, FR-29, AD-18 (matrix «Re-send, Nei»): deleted, `refused` added,
    the earlier event kept."""
    guest_id = _member(who)
    _send_allergies({guest_id: GLUTEN}, {guest_id: True}, confirmed=[guest_id], now=EARLIER)
    _send_allergies({guest_id: GLUTEN}, {guest_id: False})
    assert _allergy(guest_id) is None
    assert _events(guest_id) == [Consent.GIVEN, Consent.REFUSED]
    assert list(Consent.objects.values_list("at", flat=True)) == [EARLIER, LAST_SECOND]


@pytest.mark.parametrize("who", ["respondent", "other"])
def test_a_re_send_ja_replaces_the_data(deadline, who):
    """FR-26, AD-18 (matrix «Re-send, Ja with new data»)."""
    guest_id = _member(who)
    _send_allergies({guest_id: GLUTEN}, {guest_id: True}, confirmed=[guest_id], now=EARLIER)
    _send_allergies({guest_id: LACTOSE}, {guest_id: True}, confirmed=[guest_id])
    assert _allergy(guest_id) == {"cats": ("lactose",), "none": False, "note": ""}
    assert Allergy.objects.count() == 1
    assert _events(guest_id) == [Consent.GIVEN, Consent.GIVEN]


def test_stopping_coming_deletes_without_an_event(deadline):
    """FR-75, NFR-3 (matrix «Stops coming»): no health data for someone not
    coming, and no consent event since none was answered."""
    sigmund, bestemor = _ids(SIGMUND)
    _send_allergies({bestemor: NUTS}, {bestemor: True}, confirmed=[bestemor], now=EARLIER)
    gone = Answer({sigmund: True, bestemor: False}, True)
    _send_allergies({bestemor: NUTS}, {bestemor: True}, confirmed=[bestemor], answer=gone)
    assert _allergy(bestemor) is None
    assert _events(bestemor) == [Consent.GIVEN]


def test_a_refused_send_writes_no_allergy_data(deadline):
    """AD-3, FR-41 (matrix «Refused send»): other household, admin, deadline."""
    sigmund, _ = _ids(SIGMUND)
    answer = _with(_sigmund_answer(), {sigmund: GLUTEN}, {sigmund: True})
    couple = User.objects.create(username="par-test", role=User.Role.COUPLE)
    attempts = [
        (_actor(ARILD), LAST_SECOND, NotAllowed),
        (AdminActor(couple), LAST_SECOND, NotAllowed),
        (_actor(SIGMUND), CLOSED, DeadlinePassed),
    ]
    for actor, now, error in attempts:
        with pytest.raises(error):
            _send(actor, SIGMUND, sigmund, answer, now=now)
    assert (Allergy.objects.count(), Consent.objects.count()) == (0, 0)


def test_the_allergy_models_store_facts_only():
    """AD-4, AD-18, FR-29: one boolean per category and no derived field; the
    consent row has room for `withdrawn` and the couple (Stories 7.2, 4.4)."""
    allergy_fields = {field.name for field in Allergy._meta.get_fields()}
    assert allergy_fields == {"id", "guest", *ALLERGY_KEYS, "none", "note"}
    consent_fields = {field.name for field in Consent._meta.get_fields()}
    assert consent_fields == {
        "id",
        "guest",
        "event",
        "at",
        "given_by",
        "given_by_user",
        "given_by_name",
        "text_version",
    }
    assert [key for key, _ in Consent.EVENTS] == ["given", "refused", "withdrawn"]


def test_no_names_or_notes_in_str_or_logs(deadline, caplog):
    """NFR-3: `str()` and the log hold no name, category or note."""
    sigmund, _ = _ids(SIGMUND)
    with caplog.at_level(logging.DEBUG):
        _send_allergies({sigmund: GLUTEN}, {sigmund: True})
    for text in (str(Allergy.objects.get()), str(Consent.objects.get()), caplog.text):
        for word in ("Sigmund", "gluten", "Gluten", "Tåler"):
            assert word not in text


def _all_rows() -> tuple:
    """Every row a send writes, so a test can check that a refusal wrote nothing."""
    return (
        _counts(),
        list(PersonAnswer.objects.values_list()),
        list(Allergy.objects.values_list()),
        Consent.objects.count(),
        Submission.objects.count(),
    )


def test_a_first_send_records_its_submission(deadline):
    """AD-20, NFR-1 (Story 2.6c, matrix «First send»): one `Submission` of kind
    `answer` naming the `HouseholdAnswer`, at `now`; revision 0 to 1."""
    sigmund, _ = _ids(SIGMUND)
    key = uuid.uuid4()
    sent = _send(_actor(SIGMUND), SIGMUND, sigmund, _sigmund_answer(), submission=key)
    submission = Submission.objects.get()
    assert (submission.key, submission.kind, submission.object_id) == (key, "answer", sent.pk)
    assert submission.created_at == LAST_SECOND
    assert Guest.objects.get(code=SIGMUND).household.revision == 1
    assert submitted(Guest.objects.get(code=SIGMUND).household, key)
    assert not submitted(Guest.objects.get(code=ARILD).household, key)


def test_a_repeat_returns_the_earlier_answer(deadline):
    """AD-20, NFR-1 (Story 2.6c, matrix «Double tap»): the same id again returns
    the same `HouseholdAnswer` and writes nothing: no new `Consent`, no
    `PersonAnswer` change, no revision bump, even at an old revision."""
    sigmund, _ = _ids(SIGMUND)
    key = uuid.uuid4()
    answer = _with(_sigmund_answer(), {sigmund: GLUTEN}, {sigmund: True})
    first = _send(_actor(SIGMUND), SIGMUND, sigmund, answer, submission=key)
    before = _all_rows()
    again = _send(
        _actor(SIGMUND),
        SIGMUND,
        sigmund,
        Answer({sigmund: False, sigmund + 1: False}, True),
        submission=key,
        revision=0,
        shown_total=999,
    )
    assert again.pk == first.pk
    assert _all_rows() == before
    assert Guest.objects.get(code=SIGMUND).household.revision == 1


def test_a_repeat_after_a_re_send_returns_the_re_send(deadline):
    """AD-20 (Story 2.6c, matrix «Double tap»): the answer is one row per
    household, so a repeat of the re-send's id returns it as updated."""
    sigmund, bestemor = _ids(SIGMUND)
    earlier = LAST_SECOND - datetime.timedelta(hours=1)
    _send(_actor(SIGMUND), SIGMUND, sigmund, _sigmund_answer(), now=earlier)
    key = uuid.uuid4()
    _send(_actor(SIGMUND), SIGMUND, bestemor, _sigmund_answer(), submission=key)
    again = _send(_actor(SIGMUND), SIGMUND, sigmund, _sigmund_answer(), submission=key)
    assert (again.sent_by_name, again.sent_at) == ("bestemor", LAST_SECOND)
    assert Submission.objects.count() == 2
    assert Guest.objects.get(code=SIGMUND).household.revision == 2


def test_another_households_key_is_refused(deadline):
    """AD-3, AD-20 (Story 2.6c, matrix «Key of another household»): an id written
    for Arild's household is `NotAllowed` for Sigmund's, writing nothing."""
    arild, marie, filippa, leone = _ids(ARILD)
    key = uuid.uuid4()
    nobody = Answer({arild: False, marie: False, filippa: False, leone: False}, True)
    _send(_actor(ARILD), ARILD, arild, nobody, submission=key)
    sigmund, _ = _ids(SIGMUND)
    before = _all_rows()
    with pytest.raises(NotAllowed):
        _send(_actor(SIGMUND), SIGMUND, sigmund, _sigmund_answer(), submission=key)
    assert _all_rows() == before


def test_two_sends_from_the_same_revision(deadline):
    """AD-9, NFR-1 (Story 2.6c, matrix «Two tabs / devices»): the first writes;
    the second, also from revision 0, is `RevisionConflict` with revision 1
    and writes nothing; a retry at revision 1 is a new send."""
    sigmund, bestemor = _ids(SIGMUND)
    _send(_actor(SIGMUND), SIGMUND, sigmund, _sigmund_answer(), revision=0)
    before = _all_rows()
    with pytest.raises(RevisionConflict) as refused:
        _send(_actor(SIGMUND), SIGMUND, bestemor, _sigmund_answer(), revision=0)
    assert refused.value.revision == 1
    assert _all_rows() == before
    _send(_actor(SIGMUND), SIGMUND, bestemor, _sigmund_answer(), revision=1)
    assert HouseholdAnswer.objects.get().sent_by_name == "bestemor"
    assert Submission.objects.count() == 2


@pytest.mark.parametrize(
    ("checks", "now", "error"),
    [
        ({"revision": 3}, LAST_SECOND, RevisionConflict),
        ({"shown_total": 1}, LAST_SECOND, TotalChanged),
        ({"consent_version": "2020-01-01"}, LAST_SECOND, ConsentTextChanged),
        ({"consent_version": None}, LAST_SECOND, ConsentTextChanged),
        ({}, CLOSED, DeadlinePassed),
        ({"revision": 3}, CLOSED, RevisionConflict),
    ],
    ids=["revision", "total", "consent text", "no consent text", "deadline", "revision first"],
)
def test_a_refused_send_records_no_submission(deadline, checks, now, error):
    """AD-7, AD-9, AD-18, AD-20 (Story 2.6c, matrix «Price changed», «Consent
    text changed»): each refusal leaves every row and the revision unchanged
    and records no `Submission`."""
    sigmund, _ = _ids(SIGMUND)
    answer = _with(_sigmund_answer(), {sigmund: GLUTEN}, {sigmund: True})
    before = _all_rows()
    with pytest.raises(error):
        _send(_actor(SIGMUND), SIGMUND, sigmund, answer, now=now, **checks)
    assert _all_rows() == before
    assert Submission.objects.count() == 0


def test_a_price_change_is_refused(deadline):
    """AD-7, NFR-2 (Story 2.6c, matrix «Price changed»): the total shown before
    the cabin price rose no longer matches."""
    sigmund, _ = _ids(SIGMUND)
    shown = household_total(_sigmund_answer(), form_prices())
    Settings.objects.filter(pk=1).update(price_cabin_weekend=F("price_cabin_weekend") + 100)
    with pytest.raises(TotalChanged):
        _send(_actor(SIGMUND), SIGMUND, sigmund, _sigmund_answer(), shown_total=shown)
    assert HouseholdAnswer.objects.count() == 0


def test_without_a_consent_answer_the_text_version_is_not_checked(deadline):
    """AD-18 (Story 2.6c, matrix «Text changed, no consent answered»): `cv` None
    and no consent answer sends."""
    sigmund, _ = _ids(SIGMUND)
    _send(_actor(SIGMUND), SIGMUND, sigmund, _sigmund_answer(), consent_version=None)
    assert HouseholdAnswer.objects.count() == 1


def test_the_submission_model():
    """AD-20, AD-4 (Story 2.6c): the id, the kind, what was written and when;
    `str()` without a name."""
    fields = {field.name for field in Submission._meta.get_fields()}
    assert fields == {"id", "key", "kind", "object_id", "created_at"}
    assert Submission._meta.get_field("key").unique
    assert [key for key, _ in Submission.KINDS] == [Submission.ANSWER] == ["answer"]
    submission = Submission(pk=7, key=uuid.uuid4(), kind=Submission.ANSWER, object_id=1)
    assert str(submission) == "Innsending 7"
