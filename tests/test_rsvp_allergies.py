"""Allergies and consent: step 5 (Story 2.4).

FR-22, FR-25, FR-26, FR-27, FR-28, FR-75, AD-1, AD-8, AD-18, UX-DR16,
UX-DR21, UX-DR52. Every row of the story's I/O matrix over HTTP for Sigmund
and Arild's households, the epics AC (consent «Ja» for someone else with
information and no confirmation is a field error), where the confirmation
shows before and after «Bytt», the consent radios starting unanswered, the
consent text once and its version paired with a hash, the one script, Enter
as «Fortsett», and a walk through steps 1 to 5 that writes nothing and is
never cached. The rules are in test_allergy_rules.py; the browser runs are
MT-33 to MT-35 in docs/manual-test-plan.md.
"""

import hashlib
import re
from pathlib import Path

import pytest
from django.contrib.sessions.models import Session
from django.core import signing
from django.test import Client

from tests.helpers import checked_radios, page_text, row_counts, ticked_boxes
from wedding.models import Guest
from wedding.rsvp.draft import COOKIE_NAME, SALT
from wedding.services.consent import CONSENT_TEXT_VERSION

SIGMUND = "test-sigmund0000000000"
ARILD = "test-arild000000000000"
CONSENT_TEMPLATE = (
    Path(__file__).resolve().parent.parent
    / "wedding"
    / "rsvp"
    / "templates"
    / "rsvp"
    / "includes"
    / "consent_text.html"
)
# AD-18: the consent text's version and the sha256 of its template. A change to
# the text fails this pair until both the version and the hash are updated.
CONSENT_PAIR = (
    "2026-11-23",
    "67439797dc41f985ad5f227ddc8f95c4b52ce73eb5c5526dc173f95476840a6b",
)

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


def _ids(code: str) -> list[int]:
    household = Guest.objects.get(code=code).household
    return list(household.guests.order_by("id").values_list("id", flat=True))


def _url(code: str, slug: str = "") -> str:
    return f"/{code}/svar/{slug}/" if slug else f"/{code}/svar/"


def _draft(response) -> dict:
    return signing.loads(response.cookies[COOKIE_NAME].value, salt=SALT)


def _links(html: str) -> list[tuple[str, str]]:
    return re.findall(r'<li>\s*<a href="(#[^"]+)">([^<]+)</a>\s*</li>', html)


def _person_groups(html: str) -> list[str]:
    """Each person's part of step 5, from their fieldset to the next one or the actions."""
    start = '<fieldset class="form-group allergy-group"'
    end = html.index('<div class="form-actions">')
    return html[:end].split(start)[1:]


def _sigmund_to_allergies(client) -> tuple[int, int]:
    """Both «Kommer», the whole weekend, nobody staying, no meals."""
    sigmund, bestemor = _ids(SIGMUND)
    client.post(_url(SIGMUND), {f"attendance_{sigmund}": "yes", f"attendance_{bestemor}": "yes"})
    client.post(_url(SIGMUND, "dager"), {"whole": "yes"})
    client.post(
        _url(SIGMUND, "overnatting"), {f"overnight_{sigmund}": "no", f"overnight_{bestemor}": "no"}
    )
    response = client.post(_url(SIGMUND, "maltider"), {"action": "continue"})
    assert response["Location"] == _url(SIGMUND, "allergier")
    return sigmund, bestemor


def _arild_to_allergies(client) -> list[int]:
    """Everyone in Arild's household «Kommer», the whole weekend, nobody staying."""
    ids = _ids(ARILD)
    client.post(_url(ARILD), {f"attendance_{guest_id}": "yes" for guest_id in ids})
    client.post(_url(ARILD, "dager"), {"whole": "yes"})
    client.post(_url(ARILD, "overnatting"), {f"overnight_{guest_id}": "no" for guest_id in ids})
    response = client.post(_url(ARILD, "maltider"), {"action": "continue"})
    assert response["Location"] == _url(ARILD, "allergier")
    return ids


def _post(client, data: dict, code: str = SIGMUND):
    return client.post(_url(code, "allergier"), data)


# The page


def test_the_page_without_javascript(client, seeded):
    """FR-25 to FR-27 (AC 2): «Steg 5 av 6», the consent text once, a group per
    person with «Ingen …», seven categories, the note, unanswered «Ja»/«Nei», and
    the confirmation only in bestemor's group; no total and no warning."""
    sigmund, bestemor = _sigmund_to_allergies(client)
    response = client.get(_url(SIGMUND, "allergier"))
    assert response.status_code == 200
    html = response.content.decode()
    text = page_text(html)
    assert '<h1 id="sporsmal">Allergier og matbehov</h1>' in html
    assert "Steg 5 av 6: Allergier og matbehov" in text
    assert "Dette er valgfritt." in text
    assert html.count('id="samtykke-tekst"') == 1
    for phrase in (
        "bare for at kjøkkenet skal lage mat dere tåler",
        "Rikke og Valdemar, toastmaster og forloverne kan se dem.",
        "sendes til kjøkkenet på Hardingasete",
        "trekke samtykket tilbake når som helst med den samme lenken",
        "Dere kan sende svaret også uten å samtykke.",
    ):
        assert text.count(phrase) == 1, phrase
    groups = _person_groups(html)
    assert len(groups) == 2
    for guest_id, name, group in (
        (sigmund, "Sigmund", groups[0]),
        (bestemor, "bestemor", groups[1]),
    ):
        group_text = page_text(group)
        assert f"<legend>{name}</legend>" in group
        assert "Ingen allergier eller matbehov" in group_text
        assert "Eller kryss av for det som gjelder:" in group_text
        for label in ("Gluten", "Laktose", "Nøtter", "Skalldyr", "Vegetar", "Veganer", "Annet"):
            assert f"{label} " in group_text + " ", label
        assert f'<label class="text-field__label" for="note_{guest_id}">' in group
        assert f"Kort merknad om {name} (valgfritt)" in group_text
        assert "Skriv bare det kjøkkenet trenger å vite, ingen diagnoser. Høyst 200 tegn." in (
            group_text
        )
        assert 'maxlength="200"' in group
        assert 'rows="4"' in group
        assert f"Får vi lagre opplysningene om {name}?" in group_text
        assert 'aria-describedby="samtykke-tekst"' in group
        assert f'id="consent_{guest_id}_yes"' in group
        assert f'id="consent_{guest_id}_no"' in group
    assert "Jeg bekrefter" not in groups[0]
    assert "Jeg bekrefter at bestemor vet om dette og er enig" in page_text(groups[1])
    assert checked_radios(html) == {"respondent": str(sigmund)}
    assert ticked_boxes(html) == []
    assert "Totalt" not in text
    assert "Obs:" not in text
    assert not re.search(r"\d\s*kr\b", text)


def test_every_input_is_labelled(client, seeded):
    """WCAG 1.3.1, 3.3.2: every checkbox and radio is inside a label, and the note
    has a `label for`."""
    _sigmund_to_allergies(client)
    html = client.get(_url(SIGMUND, "allergier")).content.decode()
    fields = html[html.index('id="samtykke-tekst"') :]
    inputs = re.findall(r"<input\b[^>]*>", fields)
    # «Ingen», 7 categories and «Ja»/«Nei» each, and bestemor's confirmation.
    assert len(inputs) == 2 * 10 + 1
    labelled = re.findall(r'<label class="choice[^"]*">\s*<input\b', fields)
    assert len(labelled) == len(inputs)


def test_exactly_one_script(client, seeded):
    """UX-DR21: step 5 has exactly one script, rsvp-allergies.js, deferred."""
    _sigmund_to_allergies(client)
    html = client.get(_url(SIGMUND, "allergier")).content.decode()
    assert html.count("<script") == 1
    assert re.search(r'<script src="/static/js/rsvp-allergies\.js" defer></script>', html)


def test_enter_submits_as_fortsett(client, seeded):
    """UX-DR18: the first button in the form is the hidden «Fortsett»."""
    _sigmund_to_allergies(client)
    html = client.get(_url(SIGMUND, "allergier")).content.decode()
    form = html[html.index("<form") :]
    first = re.search(r"<button[^>]*>[^<]*</button>", form).group(0)
    assert first == '<button type="submit" hidden>Fortsett</button>'


def test_the_consent_text_version_is_paired_with_its_text():
    """AD-18: CONSENT_TEXT_VERSION lives in wedding/services/ and changes with the
    text: this pair is the version and the template's sha256."""
    digest = hashlib.sha256(CONSENT_TEMPLATE.read_bytes()).hexdigest()
    assert (CONSENT_TEXT_VERSION, digest) == CONSENT_PAIR


# The I/O matrix


def test_skip_all(client, seeded):
    """FR-25: «Fortsett» with nothing ticked completes the step and goes to the hike."""
    _sigmund_to_allergies(client)
    response = _post(client, {"action": "continue"})
    assert response.status_code == 302
    assert response["Location"] == _url(SIGMUND, "fjelltur")
    draft = _draft(response)
    assert "allergies" in draft["done"]
    assert draft["alg"] == {}
    assert draft["cons"] == {}


def test_sigmund_s_journey(client, seeded):
    """FR-25 to FR-27: Sigmund «Ingen» and «Ja»; bestemor Laktose, «Ja», confirmed:
    done, and no warning when the step is opened again."""
    sigmund, bestemor = _sigmund_to_allergies(client)
    response = _post(
        client,
        {
            f"allergy_none_{sigmund}": "yes",
            f"consent_{sigmund}": "yes",
            f"allergies_{bestemor}": "lactose",
            f"consent_{bestemor}": "yes",
            f"confirm_{bestemor}": "yes",
        },
    )
    assert response["Location"] == _url(SIGMUND, "fjelltur")
    draft = _draft(response)
    assert draft["alg"] == {
        str(sigmund): {"c": [], "n": True, "t": ""},
        str(bestemor): {"c": ["lactose"], "n": False, "t": ""},
    }
    assert draft["cons"] == {str(sigmund): True, str(bestemor): True}
    assert draft["conf"] == [bestemor]
    html = client.get(_url(SIGMUND, "allergier")).content.decode()
    assert "Obs:" not in page_text(html)
    assert checked_radios(html)[f"consent_{bestemor}"] == "yes"
    assert ticked_boxes(html) == [
        f"allergy_none_{sigmund}",
        f"allergies_{bestemor}_lactose",
        f"confirm_{bestemor}",
    ]


@pytest.mark.parametrize("by", ["category", "note"])
def test_conflict(client, seeded, by):
    """FR-22, UX-DR21: «Ingen» with a category or a note: `?feil=1`, both kept, the
    error under bestemor's legend, the summary link to her «Ingen», title «Feil: »."""
    _, bestemor = _sigmund_to_allergies(client)
    data = {f"allergy_none_{bestemor}": "yes"}
    data |= (
        {f"allergies_{bestemor}": "lactose"}
        if by == "category"
        else {f"note_{bestemor}": "ikke koriander"}
    )
    response = _post(client, data)
    assert response.status_code == 303
    assert response["Location"] == f"{_url(SIGMUND, 'allergier')}?feil=1"
    draft = _draft(response)
    assert "allergies" not in draft["done"]
    assert draft["alg"][str(bestemor)]["n"] is True
    html = client.get(response["Location"]).content.decode()
    assert re.search(r"<title>\s*Feil: ", html)
    assert _links(html) == [(f"#allergy_none_{bestemor}", "Rett opp allergiene for bestemor")]
    group = _person_groups(html)[1]
    assert f'aria-describedby="allergy_none_{bestemor}_error"' in group
    assert (
        "Feil: Du har krysset av for «Ingen allergier eller matbehov» og fylt inn noe annet "
        "for bestemor. Velg det ene."
    ) in page_text(group)
    assert f"allergy_none_{bestemor}" in ticked_boxes(html)
    if by == "category":
        assert f"allergies_{bestemor}_lactose" in ticked_boxes(html)
    else:
        assert ">ikke koriander</textarea>" in group


def test_missing_confirmation(client, seeded):
    """FR-27, epics AC: consent «Ja» for bestemor with Laktose and no confirmation is
    a field error on the confirmation, with the summary link «Bekreft for bestemor»."""
    _, bestemor = _sigmund_to_allergies(client)
    response = _post(client, {f"allergies_{bestemor}": "lactose", f"consent_{bestemor}": "yes"})
    assert response.status_code == 303
    html = client.get(response["Location"]).content.decode()
    assert _links(html) == [(f"#confirm_{bestemor}", "Bekreft for bestemor")]
    confirm = re.search(rf'<input\b[^>]*id="confirm_{bestemor}"[^>]*>', html).group(0)
    assert 'aria-invalid="true"' in confirm
    assert f'aria-describedby="confirm_{bestemor}_error"' in confirm
    assert f'<p class="field-error" id="confirm_{bestemor}_error">' in html
    assert (
        "Feil: Kryss av for at bestemor vet om dette og er enig, eller svar «Nei» på "
        "samtykket." in page_text(html)
    )


@pytest.mark.parametrize(
    "data",
    [
        {"consent_SIGMUND": "yes", "allergies_SIGMUND": "nuts"},
        {"consent_BESTEMOR": "yes"},
        {"consent_BESTEMOR": "no", "allergies_BESTEMOR": "lactose"},
        {"allergies_BESTEMOR": "lactose"},
    ],
    ids=["respondent's own Ja", "Ja with no info", "Nei", "unanswered"],
)
def test_confirmation_not_needed(client, seeded, data):
    """FR-27: no confirmation for the respondent, for «Ja» with no info, or without «Ja»."""
    sigmund, bestemor = _sigmund_to_allergies(client)
    posted = {
        key.replace("SIGMUND", str(sigmund)).replace("BESTEMOR", str(bestemor)): value
        for key, value in data.items()
    }
    response = _post(client, posted)
    assert response["Location"] == _url(SIGMUND, "fjelltur")


@pytest.mark.parametrize("consent", [None, "no"])
def test_no_consent_goes_on_and_warns(client, seeded, consent):
    """FR-28 (AC 4): bestemor Laktose with consent unanswered or «Nei» goes on; step 5
    opened again shows the warning naming bestemor, and «Fortsett» still goes on."""
    _, bestemor = _sigmund_to_allergies(client)
    data = {f"allergies_{bestemor}": "lactose"}
    if consent:
        data[f"consent_{bestemor}"] = consent
    response = _post(client, data)
    assert response["Location"] == _url(SIGMUND, "fjelltur")
    assert _draft(response)["alg"][str(bestemor)]["c"] == ["lactose"]
    html = client.get(_url(SIGMUND, "allergier")).content.decode()
    warning = (
        "Obs: Allergiopplysningene om bestemor blir ikke lagret uten et «Ja» til samtykke. "
        "Dere kan sende svaret likevel, og heller si fra til oss direkte."
    )
    assert warning in page_text(html)
    notice = re.search(r'<div class="notice notice--warning"[^>]*>', html).group(0)
    assert "role=" not in notice
    assert "autofocus" not in notice
    assert html.index("notice--warning") < html.index('class="form-group allergy-group"')
    assert _post(client, data)["Location"] == _url(SIGMUND, "fjelltur")


def test_the_warning_names_several(client, seeded):
    """FR-28: names joined with «, » and « og », in household order."""
    arild, marie, _, leone = _arild_to_allergies(client)
    _post(
        client,
        {
            f"allergy_none_{arild}": "yes",
            f"allergies_{marie}": "nuts",
            f"note_{leone}": "liker ikke fisk",
        },
        ARILD,
    )
    html = client.get(_url(ARILD, "allergier")).content.decode()
    assert "Allergiopplysningene om Arild, Marie og Leone blir ikke lagret" in page_text(html)


@pytest.mark.parametrize(("length", "kept"), [(200, True), (201, False)])
def test_note_200_and_201(client, seeded, length, kept):
    """FR-25: a 200-character note with æøå is kept; a 201-character one (forged past
    `maxlength`) never reaches the cookie, the previous note stays, and `?feil=1`
    shows the error between the label and the field."""
    _, bestemor = _sigmund_to_allergies(client)
    _post(client, {f"note_{bestemor}": "før"})
    client.get(_url(SIGMUND, "allergier"))
    note = ("æøå " * 70)[: length - 1] + "x"
    assert len(note) == length
    response = _post(client, {f"note_{bestemor}": note})
    draft = _draft(response)
    assert note not in response.cookies[COOKIE_NAME].value
    if kept:
        assert response["Location"] == _url(SIGMUND, "fjelltur")
        assert draft["alg"][str(bestemor)]["t"] == note
        assert draft["long"] == []
        return
    assert response.status_code == 303
    assert draft["alg"][str(bestemor)]["t"] == "før"
    assert draft["long"] == [bestemor]
    assert "allergies" not in draft["done"]
    html = client.get(response["Location"]).content.decode()
    assert _links(html) == [(f"#note_{bestemor}", "Kort ned merknaden om bestemor")]
    group = _person_groups(html)[1]
    label = group.index(f'for="note_{bestemor}"')
    error = group.index(f'id="note_{bestemor}_error"')
    field = group.index("<textarea")
    assert label < error < field
    assert "Feil: Merknaden om bestemor kan være høyst 200 tegn." in page_text(group)
    assert "text-field--error" in group
    textarea = re.search(r"<textarea\b[^>]*>", group).group(0)
    assert 'aria-invalid="true"' in textarea
    assert f'aria-describedby="note_{bestemor}_hint note_{bestemor}_error"' in textarea
    # The next allergies write clears the marker.
    response = _post(client, {f"note_{bestemor}": "kort"})
    assert response["Location"] == _url(SIGMUND, "fjelltur")
    assert _draft(response)["long"] == []


def test_whitespace_note(client, seeded):
    """FR-25: a note of spaces is stored as nothing."""
    _, bestemor = _sigmund_to_allergies(client)
    response = _post(client, {f"note_{bestemor}": "   "})
    assert response["Location"] == _url(SIGMUND, "fjelltur")
    assert _draft(response)["alg"] == {}


def test_forged_values_are_ignored(client, seeded):
    """FR-25 to FR-27: an unknown category, consent «maybe», a confirmation other than
    «yes» and a non-coming person's fields are ignored."""
    arild, marie, filippa, leone = _ids(ARILD)
    client.post(
        _url(ARILD),
        {
            f"attendance_{arild}": "yes",
            f"attendance_{marie}": "yes",
            f"attendance_{filippa}": "yes",
            f"attendance_{leone}": "no",
        },
    )
    client.post(_url(ARILD, "dager"), {"whole": "yes"})
    client.post(
        _url(ARILD, "overnatting"),
        {f"overnight_{guest_id}": "no" for guest_id in (arild, marie, filippa)},
    )
    client.post(_url(ARILD, "maltider"), {"action": "continue"})
    response = _post(
        client,
        {
            f"allergies_{marie}": ["fish", "nuts"],
            f"consent_{marie}": "maybe",
            f"confirm_{marie}": "on",
            f"allergies_{leone}": "nuts",
            f"consent_{leone}": "yes",
            f"confirm_{leone}": "yes",
        },
        ARILD,
    )
    assert response["Location"] == _url(ARILD, "fjelltur")
    draft = _draft(response)
    assert draft["alg"] == {str(marie): {"c": ["nuts"], "n": False, "t": ""}}
    assert draft["cons"] == {}
    assert draft["conf"] == []


def test_someone_who_stops_coming_loses_their_allergy_data(client, seeded):
    """FR-75: bestemor «Kommer ikke» on step 1 drops her entry, consent and
    confirmation."""
    sigmund, bestemor = _sigmund_to_allergies(client)
    _post(
        client,
        {
            f"allergy_none_{sigmund}": "yes",
            f"allergies_{bestemor}": "lactose",
            f"consent_{bestemor}": "yes",
            f"confirm_{bestemor}": "yes",
        },
    )
    response = client.post(
        _url(SIGMUND), {f"attendance_{sigmund}": "yes", f"attendance_{bestemor}": "no"}
    )
    draft = _draft(response)
    assert draft["alg"] == {str(sigmund): {"c": [], "n": True, "t": ""}}
    assert draft["cons"] == {}
    assert draft["conf"] == []
    assert "allergies" not in draft["done"]


def test_bytt_moves_the_confirmation_and_reopens_the_step(client, seeded):
    """FR-12, FR-27, UX-DR18: «Velg» keeps the posted values without validating;
    with bestemor answering, Sigmund's «Ja» with info now needs confirmation, the
    box moves to his group, and the step is no longer done."""
    sigmund, bestemor = _sigmund_to_allergies(client)
    response = _post(
        client,
        {f"allergy_none_{sigmund}": "yes", f"consent_{sigmund}": "yes"},
    )
    assert "allergies" in _draft(response)["done"]
    response = _post(
        client,
        {
            "action": "switch",
            "respondent": str(bestemor),
            f"allergy_none_{sigmund}": "yes",
            f"consent_{sigmund}": "yes",
            f"allergies_{bestemor}": "lactose",
            f"allergy_none_{bestemor}": "yes",
        },
    )
    assert response["Location"] == _url(SIGMUND, "allergier")
    draft = _draft(response)
    assert draft["resp"] == bestemor
    assert draft["alg"][str(bestemor)] == {"c": ["lactose"], "n": True, "t": ""}
    assert "allergies" not in draft["done"]
    html = client.get(_url(SIGMUND, "allergier")).content.decode()
    groups = _person_groups(html)
    assert "Jeg bekrefter at Sigmund vet om dette og er enig" in page_text(groups[0])
    assert "Jeg bekrefter" not in groups[1]
    assert client.get(_url(SIGMUND, "fjelltur"))["Location"] == _url(SIGMUND, "allergier")


def test_csrf_failure_keeps_what_was_posted(seeded):
    """UX-DR52: 403 with the posted ticks, note, consent and confirmation, a focused
    notice, no errors and no draft written."""
    client = Client()
    _, bestemor = _sigmund_to_allergies(client)
    client.handler.enforce_csrf_checks = True
    response = _post(
        client,
        {
            f"allergies_{bestemor}": "lactose",
            f"allergy_none_{bestemor}": "yes",
            f"note_{bestemor}": "x" * 201,
            f"consent_{bestemor}": "yes",
        },
    )
    assert response.status_code == 403
    assert COOKIE_NAME not in response.cookies
    html = response.content.decode()
    assert "Prøv igjen." in page_text(html)
    assert re.search(r'<div class="notice notice--error"[^>]*autofocus', html)
    assert "error-summary" not in html
    assert "field-error" not in html
    assert checked_radios(html)[f"consent_{bestemor}"] == "yes"
    assert ticked_boxes(html) == [f"allergy_none_{bestemor}", f"allergies_{bestemor}_lactose"]
    assert f">{'x' * 201}</textarea>" in html
    assert html.count("<script") == 1


def test_a_format_3_draft_is_deleted(client, seeded):
    """AD-8: a Story 2.3 cookie is broken: deleted, and the form starts at step 1."""
    sigmund, bestemor = _ids(SIGMUND)
    client.cookies[COOKIE_NAME] = signing.dumps(
        {
            "v": 3,
            "started": "2026-11-21T10:00:00+00:00",
            "rev": 0,
            "resp": sigmund,
            "att": {str(sigmund): True, str(bestemor): True},
            "done": ["who", "days", "overnight", "meals"],
            "whole": True,
            "days": {},
            "night": {str(sigmund): False, str(bestemor): False},
            "meals": {},
        },
        salt=SALT,
        compress=True,
    )
    response = client.get(_url(SIGMUND, "allergier"))
    assert response["Location"] == _url(SIGMUND)
    assert response.cookies[COOKIE_NAME]["max-age"] == 0


def test_arild_s_errors_for_two_people(client, seeded):
    """FR-22, MT-35's state: CONFLICT for Marie and CONFIRM for Filippa, linked in
    page order."""
    _, marie, filippa, _ = _arild_to_allergies(client)
    response = _post(
        client,
        {
            f"allergy_none_{marie}": "yes",
            f"allergies_{marie}": "gluten",
            f"allergies_{filippa}": "vegan",
            f"consent_{filippa}": "yes",
        },
        ARILD,
    )
    html = client.get(response["Location"]).content.decode()
    assert _links(html) == [
        (f"#allergy_none_{marie}", "Rett opp allergiene for Marie"),
        (f"#confirm_{filippa}", "Bekreft for Filippa"),
    ]
    groups = _person_groups(html)
    assert len(groups) == 4
    assert "Jeg bekrefter" not in groups[0]


def test_the_walk_writes_nothing_and_is_never_cached(client, seeded):
    """AD-1, AD-8, FR-3 (AC 5): steps 1 to 5 write no row, use no session and no
    messages, and every response is private and never stored."""
    before = row_counts()
    sigmund, bestemor = _ids(SIGMUND)
    requests = [
        ("get", _url(SIGMUND), {}),
        ("post", _url(SIGMUND), {f"attendance_{sigmund}": "yes", f"attendance_{bestemor}": "yes"}),
        ("post", _url(SIGMUND, "dager"), {"whole": "yes"}),
        (
            "post",
            _url(SIGMUND, "overnatting"),
            {f"overnight_{sigmund}": "no", f"overnight_{bestemor}": "no"},
        ),
        ("post", _url(SIGMUND, "maltider"), {"action": "continue"}),
        ("get", _url(SIGMUND, "allergier"), {}),
        ("post", _url(SIGMUND, "allergier"), {f"allergies_{bestemor}": "lactose"}),
        ("get", _url(SIGMUND, "allergier"), {}),
        (
            "post",
            _url(SIGMUND, "allergier"),
            {f"allergy_none_{bestemor}": "yes", f"allergies_{bestemor}": "lactose"},
        ),
        ("get", f"{_url(SIGMUND, 'allergier')}?feil=1", {}),
    ]
    for method, path, data in requests:
        response = getattr(client, method)(path, data)
        assert response.status_code in (200, 302, 303), (method, path)
        assert "private" in response["Cache-Control"]
        assert "no-store" in response["Cache-Control"]
        assert "sessionid" not in response.cookies
        assert "messages" not in response.cookies
    assert row_counts() == before
    assert Session.objects.count() == 0
