"""The Friday hike and the check page (Story 2.5).

FR-17, FR-21, FR-22, FR-28, FR-33, FR-75, AD-1, AD-7, AD-8, AD-12, UX-DR16,
UX-DR23, UX-DR52. Every row of the story's I/O matrix over HTTP for Sigmund
and Arild's households: step 6 only for people present on Friday, skipped
and not counted when nobody comes Friday, its errors and «Velg»; the check
page's order (notice, `h1`, one block per applicable step, the total from
`household_total`, «Send svaret» above «Tilbake»), «Ikke oppgitt», the FR-28
warning, each «Endre» link and its return with `?fra=se-over`; a POST to the
check page without `action=send` writes nothing, and a walk through steps 1
to 6 and the check page, stopping before the send, writes no row and is never
cached. Sending itself is tested in test_rsvp_send.py (Story 2.6a). The rule
is in test_answer_rules.py; the browser runs are MT-36 to MT-38 in docs/manual-test-plan.md.
"""

import re

import pytest
from django.contrib.sessions.models import Session
from django.core import signing
from django.test import Client

from tests.helpers import checked_radios, page_text, row_counts
from wedding.models import Guest
from wedding.rsvp.draft import COOKIE_NAME, SALT
from wedding.rules.answer import Answer
from wedding.rules.money import household_total
from wedding.selectors import form_prices
from wedding.templatetags.money import kroner

SIGMUND = "test-sigmund0000000000"
ARILD = "test-arild000000000000"
FROM = "?fra=se-over"
NOTICE = "Obs: Svaret er ikke sendt ennå."

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


def _title(html: str) -> str:
    return re.search(r"<title>(.*?)</title>", html, re.DOTALL).group(1).strip()


def _sigmund_to_hike(client, *, bestemor_lactose: bool = True) -> tuple[int, int]:
    """MT-36: both «Kommer», the whole weekend, both cabin, no meals, Laktose for
    bestemor without consent."""
    sigmund, bestemor = _ids(SIGMUND)
    client.post(_url(SIGMUND), {f"attendance_{sigmund}": "yes", f"attendance_{bestemor}": "yes"})
    client.post(_url(SIGMUND, "dager"), {"whole": "yes"})
    client.post(
        _url(SIGMUND, "overnatting"),
        {f"overnight_{sigmund}": "yes", f"overnight_{bestemor}": "yes"},
    )
    client.post(_url(SIGMUND, "maltider"), {"action": "continue"})
    data = {f"allergies_{bestemor}": "lactose"} if bestemor_lactose else {}
    response = client.post(_url(SIGMUND, "allergier"), data | {"action": "continue"})
    assert response["Location"] == _url(SIGMUND, "fjelltur")
    return sigmund, bestemor


def _sigmund_to_check(client) -> tuple[int, int]:
    """MT-36 b): Sigmund «Kanskje», bestemor «Nei»."""
    sigmund, bestemor = _sigmund_to_hike(client)
    response = client.post(
        _url(SIGMUND, "fjelltur"), {f"hike_{sigmund}": "maybe", f"hike_{bestemor}": "no"}
    )
    assert response["Location"] == _url(SIGMUND, "se-over")
    return sigmund, bestemor


def _arild_to_hike(client) -> list[int]:
    """MT-36 f): Arild, Marie and Filippa «Kommer», Leone not; Arild and Marie all
    days, Filippa only Saturday; nobody staying, no meals, no allergies."""
    arild, marie, filippa, leone = ids = _ids(ARILD)
    client.post(
        _url(ARILD),
        {
            f"attendance_{arild}": "yes",
            f"attendance_{marie}": "yes",
            f"attendance_{filippa}": "yes",
            f"attendance_{leone}": "no",
        },
    )
    client.post(_url(ARILD, "dager"), {"whole": "no"})
    client.post(
        _url(ARILD, "dager"),
        {
            "whole": "no",
            f"days_{arild}": ["fri", "sat", "sun"],
            f"days_{marie}": ["fri", "sat", "sun"],
            f"days_{filippa}": ["sat"],
        },
    )
    client.post(
        _url(ARILD, "overnatting"),
        {f"overnight_{arild}": "no", f"overnight_{marie}": "no", f"overnight_{filippa}": "no"},
    )
    client.post(_url(ARILD, "maltider"), {"action": "continue"})
    response = client.post(_url(ARILD, "allergier"), {"action": "continue"})
    assert response["Location"] == _url(ARILD, "fjelltur")
    return ids


def _blocks(html: str) -> list[str]:
    """Each check-page block, from its `<li>` to the next."""
    start = html.index('<ul class="check-list">')
    end = html.index("</ul>", start)
    return html[start:end].split('<li class="check-list__item">')[1:]


def _headings(html: str) -> list[str]:
    return re.findall(r"<h2>([^<]+)</h2>", html)


# Step 6


def test_the_hike_step(client, seeded):
    """FR-17 (AC): a «Ja»/«Nei»/«Kanskje» group for each, nothing checked, the
    lead, «Steg 6 av 6: Fjelltur fredag», no total and no price."""
    sigmund, bestemor = _sigmund_to_hike(client)
    html = client.get(_url(SIGMUND, "fjelltur")).content.decode()
    assert '<p class="form-progress">Steg 6 av 6: Fjelltur fredag</p>' in html
    assert _title(html) == "Steg 6 av 6: Fjelltur fredag \N{EN DASH} Invitasjon"
    text = page_text(html)
    assert (
        "Fjellturen er fredag, for dem som kommer tidlig. Svar «Kanskje» hvis dere ikke "
        "har bestemt dere ennå." in text
    )
    for guest_id in (sigmund, bestemor):
        assert re.findall(rf'id="hike_{guest_id}_(\w+)"', html) == ["yes", "no", "maybe"]
    assert re.findall(r"<legend>([^<]+)</legend>", html)[-2:] == ["Sigmund", "bestemor"]
    assert "Sigmund Ja Nei Kanskje bestemor Ja Nei Kanskje" in text
    assert checked_radios(html) == {"respondent": str(sigmund)}
    assert "Totalt for husstanden" not in html
    assert " kr" not in text.split("Hvem blir med")[1].split("Fortsett")[0]


def test_sigmund_s_journey_ends_on_the_check_page(client, seeded):
    """FR-17, matrix «Sigmund's journey»: «Kanskje» and «Nei» complete the step."""
    sigmund, bestemor = _sigmund_to_hike(client)
    response = client.post(
        _url(SIGMUND, "fjelltur"), {f"hike_{sigmund}": "maybe", f"hike_{bestemor}": "no"}
    )
    assert response.status_code == 302
    assert response["Location"] == _url(SIGMUND, "se-over")
    draft = _draft(response)
    assert draft["hike"] == {str(sigmund): "maybe", str(bestemor): "no"}
    assert "hike" in draft["done"]


def test_a_missing_hike_answer(client, seeded):
    """FR-22, matrix «Missing answer»: PRG to `?feil=1`, Sigmund's choice kept,
    the error line and the summary link, title «Feil: …»."""
    sigmund, bestemor = _sigmund_to_hike(client)
    response = client.post(_url(SIGMUND, "fjelltur"), {f"hike_{sigmund}": "maybe"})
    assert response.status_code == 303
    assert response["Location"] == f"{_url(SIGMUND, 'fjelltur')}?feil=1"
    assert "hike" not in _draft(response)["done"]
    html = client.get(response["Location"]).content.decode()
    assert _title(html).startswith("Feil: ")
    assert _links(html) == [(f"#hike_{bestemor}_yes", "Svar om fjellturen for bestemor")]
    assert "Feil: Velg «Ja», «Nei» eller «Kanskje» for bestemor." in page_text(html)
    assert f'aria-describedby="hike_{bestemor}_error"' in html
    assert checked_radios(html)[f"hike_{sigmund}"] == "maybe"
    assert client.get(_url(SIGMUND, "se-over"))["Location"] == _url(SIGMUND, "fjelltur")


def test_forged_hike_values_are_ignored(client, seeded):
    """FR-17, matrix «Forged value»: an unknown answer, or a field for someone not
    asked, is never kept."""
    arild, marie, filippa, leone = _arild_to_hike(client)
    response = client.post(
        _url(ARILD, "fjelltur"),
        {
            f"hike_{arild}": "perhaps",
            f"hike_{marie}": "yes",
            f"hike_{filippa}": "yes",
            f"hike_{leone}": "yes",
        },
    )
    assert response.status_code == 303
    assert _draft(response)["hike"] == {str(marie): "yes"}


def test_only_people_present_on_friday_are_asked(client, seeded):
    """FR-17 (AC), matrix «Only some Friday»: Filippa on Saturday only has no group
    and no Fjelltur line."""
    arild, marie, filippa, _ = _arild_to_hike(client)
    html = client.get(_url(ARILD, "fjelltur")).content.decode()
    assert f"hike_{arild}_yes" in html
    assert f"hike_{marie}_yes" in html
    assert f"hike_{filippa}" not in html
    client.post(_url(ARILD, "fjelltur"), {f"hike_{arild}": "yes", f"hike_{marie}": "no"})
    check = client.get(_url(ARILD, "se-over")).content.decode()
    hike = _blocks(check)[-1]
    assert "<h2>Fjelltur fredag</h2>" in hike
    assert "Arild: ja" in page_text(hike)
    assert "Marie: nei" in page_text(hike)
    assert "Filippa" not in hike


def test_nobody_on_friday_skips_the_hike(client, seeded):
    """FR-17 (AC), matrix «Nobody Friday»: step 6 is not counted, step 5 goes to the
    check page, `/fjelltur/` redirects there, and there is no Fjelltur block."""
    sigmund, bestemor = _ids(SIGMUND)
    client.post(_url(SIGMUND), {f"attendance_{sigmund}": "yes", f"attendance_{bestemor}": "yes"})
    client.post(_url(SIGMUND, "dager"), {"whole": "no"})
    client.post(
        _url(SIGMUND, "dager"),
        {"whole": "no", f"days_{sigmund}": ["sat", "sun"], f"days_{bestemor}": ["sat", "sun"]},
    )
    html = client.get(_url(SIGMUND, "overnatting")).content.decode()
    assert "Steg 3 av 5: Overnatting" in html
    client.post(
        _url(SIGMUND, "overnatting"), {f"overnight_{sigmund}": "no", f"overnight_{bestemor}": "no"}
    )
    client.post(_url(SIGMUND, "maltider"), {"action": "continue"})
    assert (
        "Steg 5 av 5: Allergier og matbehov"
        in client.get(_url(SIGMUND, "allergier")).content.decode()
    )
    response = client.post(_url(SIGMUND, "allergier"), {"action": "continue"})
    assert response["Location"] == _url(SIGMUND, "se-over")
    assert client.get(_url(SIGMUND, "fjelltur"))["Location"] == _url(SIGMUND, "se-over")
    check = client.get(_url(SIGMUND, "se-over")).content.decode()
    assert "Fjelltur fredag" not in _headings(check)
    assert f'href="{_url(SIGMUND, "allergier")}">Tilbake</a>' in check


def test_removing_friday_drops_the_hike_answer(client, seeded):
    """FR-75, matrix «Friday removed»: after a hike answer, Saturday and Sunday drop it."""
    sigmund, bestemor = _sigmund_to_check(client)
    response = client.post(
        _url(SIGMUND, "dager"),
        {
            "whole": "no",
            f"days_{sigmund}": ["sat", "sun"],
            f"days_{bestemor}": ["fri", "sat", "sun"],
        },
    )
    assert _draft(response)["hike"] == {str(bestemor): "no"}


def test_velg_on_the_hike_keeps_the_posted_answers(client, seeded):
    """FR-12, UX-DR18: «Velg» keeps the posted answers unvalidated, not done."""
    sigmund, bestemor = _sigmund_to_hike(client)
    response = client.post(
        _url(SIGMUND, "fjelltur"),
        {"action": "switch", "respondent": str(bestemor), f"hike_{sigmund}": "yes"},
    )
    assert response["Location"] == _url(SIGMUND, "fjelltur")
    draft = _draft(response)
    assert draft["resp"] == bestemor
    assert draft["hike"] == {str(sigmund): "yes"}
    assert "hike" not in draft["done"]


def test_csrf_failure_on_the_hike_keeps_the_posted_radios(seeded):
    """UX-DR52, matrix «CSRF on hike»: 403, the posted radios checked, the focused
    notice, and no draft write."""
    client = Client()
    sigmund, _ = _sigmund_to_hike(client)
    client.handler.enforce_csrf_checks = True
    response = client.post(_url(SIGMUND, "fjelltur"), {f"hike_{sigmund}": "maybe"})
    assert response.status_code == 403
    html = response.content.decode()
    assert checked_radios(html)[f"hike_{sigmund}"] == "maybe"
    assert 'tabindex="-1" autofocus' in html
    assert COOKIE_NAME not in response.cookies


def test_csrf_failure_on_the_check_page_shows_the_check_page(seeded):
    """UX-DR52 (Story 2.6a): the check page is shown again with the focused notice,
    not the generic 403 page."""
    client = Client()
    _sigmund_to_check(client)
    client.handler.enforce_csrf_checks = True
    response = client.post(_url(SIGMUND, "se-over"), {"action": "send"})
    assert response.status_code == 403
    html = response.content.decode()
    assert "Skjemaet ble ikke sendt</h1>" not in html
    assert "<h1>Se over svaret før du sender</h1>" in html


def test_a_format_4_draft_is_deleted(client, seeded):
    """AD-8, matrix «Old draft»: a format 4 cookie is deleted and the form starts at
    step 1."""
    sigmund, bestemor = _ids(SIGMUND)
    client.cookies[COOKIE_NAME] = signing.dumps(
        {
            "v": 4,
            "started": "2026-11-21T10:00:00+00:00",
            "rev": 0,
            "resp": sigmund,
            "att": {str(sigmund): True, str(bestemor): True},
            "done": ["who"],
            "whole": None,
            "days": {},
            "night": {},
            "meals": {},
            "alg": {},
            "cons": {},
            "conf": [],
            "long": [],
        },
        salt=SALT,
        compress=True,
    )
    response = client.get(_url(SIGMUND, "fjelltur"))
    assert response["Location"] == _url(SIGMUND)
    assert response.cookies[COOKIE_NAME]["max-age"] == 0


# The check page


def test_the_check_page_in_order(client, seeded):
    """FR-21, FR-33 (AC): the notice before the `h1`, the six blocks in step order
    with each person's answer, the total equal to `household_total`, «Send
    svaret» as the first button above «Tilbake», and no respondent line."""
    sigmund, bestemor = _sigmund_to_check(client)
    response = client.get(_url(SIGMUND, "se-over"))
    assert response.status_code == 200
    html = response.content.decode()
    assert _title(html) == "Se over svaret før du sender \N{EN DASH} Invitasjon"
    text = page_text(html)
    assert html.index("notice--warning") < html.index("<h1>Se over svaret før du sender</h1>")
    assert NOTICE in text
    assert _headings(html) == [
        "Hvem kommer",
        "Dager",
        "Overnatting",
        "Måltider",
        "Allergier og matbehov",
        "Fjelltur fredag",
    ]
    blocks = [page_text(block) for block in _blocks(html)]
    assert "Sigmund: kommer bestemor: kommer" in blocks[0]
    assert "Sigmund: hele helgen bestemor: hele helgen" in blocks[1]
    assert "Sigmund: hytte hele helgen bestemor: hytte hele helgen" in blocks[2]
    assert "Sigmund: ingen måltider bestemor: ingen måltider" in blocks[3]
    assert "Sigmund: Ikke oppgitt bestemor: laktose" in blocks[4]
    assert "Sigmund: kanskje bestemor: nei" in blocks[5]
    prices = form_prices()
    expected = household_total(
        Answer({sigmund: True, bestemor: True}, True, night={sigmund: True, bestemor: True}),
        prices,
    )
    assert f"Totalt for husstanden: <strong>{kroner(expected)}</strong>" in html
    assert "Totalt for husstanden: 3 000 kr" in text
    form = html[html.index("<form") :]
    first = re.search(r"<button[^>]*>[^<]*</button>", form).group(0)
    assert 'name="action" value="send">Send svaret</button>' in first
    assert form.index("Send svaret") < form.index(">Tilbake</a>")
    assert f'href="{_url(SIGMUND, "fjelltur")}">Tilbake</a>' in html
    assert "Jeg er" not in text
    # Story 2.6a: the only script is the busy state of «Send svaret».
    assert re.findall(r"<script[^>]*>", html) == [
        '<script src="/static/js/rsvp-send.js" defer></script>'[:-9]
    ]
    # AD-8: no hidden field holds an answer; Story 2.6c adds the one-time
    # submission id and the total shown (AD-7, AD-20).
    assert re.findall(r'type="hidden" name="(\w+)"', html) == [
        "csrfmiddlewaretoken",
        "innsending",
        "sum",
    ]


def test_skipped_answers_read_ikke_oppgitt_and_fr_28_warns(client, seeded):
    """FR-21, FR-28 (AC), matrix «Unconsented allergies»: bestemor's note and
    consent read «Ikke oppgitt» (muted), and the block warns about her."""
    _sigmund_to_check(client)
    html = client.get(_url(SIGMUND, "se-over")).content.decode()
    allergies = _blocks(html)[4]
    # The note is optional: an empty note gets no line (2026-11-24).
    assert "Merknad om bestemor" not in allergies
    assert '<p class="check-list__missing">Samtykke for bestemor: Ikke oppgitt</p>' in allergies
    assert '<p class="check-list__missing">Sigmund: Ikke oppgitt</p>' in allergies
    assert (
        "Obs: Allergiopplysningene om bestemor blir ikke lagret uten et «Ja» til samtykke."
        in page_text(allergies)
    )
    assert "role=" not in allergies.split("notice--warning")[1].split(">")[0]


def test_consent_and_confirmation_lines(client, seeded):
    """FR-21, FR-26, FR-27: a note, «ja» consent and the confirmation for bestemor;
    Sigmund's «Nei» to «Ingen …» brings the FR-28 warning."""
    sigmund, bestemor = _ids(SIGMUND)
    client.post(_url(SIGMUND), {f"attendance_{sigmund}": "yes", f"attendance_{bestemor}": "yes"})
    client.post(_url(SIGMUND, "dager"), {"whole": "yes"})
    client.post(
        _url(SIGMUND, "overnatting"), {f"overnight_{sigmund}": "no", f"overnight_{bestemor}": "no"}
    )
    client.post(
        _url(SIGMUND, "maltider"), {f"meals_{bestemor}": ["friday_dinner", "sunday_breakfast"]}
    )
    client.post(
        _url(SIGMUND, "allergier"),
        {
            f"allergy_none_{sigmund}": "yes",
            f"consent_{sigmund}": "no",
            f"allergies_{bestemor}": ["lactose", "nuts"],
            f"note_{bestemor}": "Ikke <b>mandler</b>\r\nheller",
            f"consent_{bestemor}": "yes",
            f"confirm_{bestemor}": "yes",
        },
    )
    client.post(_url(SIGMUND, "fjelltur"), {f"hike_{sigmund}": "yes", f"hike_{bestemor}": "no"})
    html = client.get(_url(SIGMUND, "se-over")).content.decode()
    blocks = _blocks(html)
    assert "bestemor: middag fredag og frokost søndag" in page_text(blocks[3])
    assert "Sigmund: ingen måltider" in page_text(blocks[3])
    allergies = blocks[4]
    text = page_text(allergies)
    assert "Sigmund: ingen allergier eller matbehov" in text
    assert "Samtykke for Sigmund: nei" in text
    assert "bestemor: laktose og nøtter" in text
    assert "Merknad om bestemor: Ikke &lt;b&gt;mandler&lt;/b&gt;<br>heller" in allergies
    assert "Samtykke for bestemor: ja" in text
    assert "Du har bekreftet at bestemor vet om det og er enig." in text
    assert "Du har bekreftet at Sigmund" not in text
    assert "Obs: Allergiopplysningene om Sigmund blir ikke lagret" in text


def test_a_note_without_a_category(client, seeded):
    """FR-21, FR-25: a note alone is information: «Merknad om …» and the consent line."""
    sigmund, bestemor = _sigmund_to_hike(client, bestemor_lactose=False)
    client.post(
        f"{_url(SIGMUND, 'allergier')}{FROM}",
        {f"note_{bestemor}": "Tåler ikke koriander", f"consent_{bestemor}": "no"},
    )
    client.post(_url(SIGMUND, "fjelltur"), {f"hike_{sigmund}": "yes", f"hike_{bestemor}": "no"})
    allergies = page_text(_blocks(client.get(_url(SIGMUND, "se-over")).content.decode())[4])
    assert "Merknad om bestemor: Tåler ikke koriander" in allergies
    assert "Samtykke for bestemor: nei" in allergies


def test_a_gate_redirect_keeps_fra(client, seeded):
    """UX-DR23, AD-7: «Endre» to a step whose earlier step is unfinished keeps `fra`
    on the gate redirect."""
    _sigmund_to_check(client)
    client.post(_url(SIGMUND, "dager"), {"whole": "no"})
    response = client.get(f"{_url(SIGMUND, 'fjelltur')}{FROM}")
    assert response["Location"] == f"{_url(SIGMUND, 'dager')}{FROM}"


def test_another_fra_value_is_ignored(client, seeded):
    """UX-DR23: only `fra=se-over` counts; Tilbake goes to the step before."""
    _sigmund_to_check(client)
    html = client.get(f"{_url(SIGMUND, 'maltider')}?fra=noe-annet").content.decode()
    assert f'href="{_url(SIGMUND, "overnatting")}">Tilbake</a>' in html


def test_keep_from_puts_the_fragment_last(rf):
    """UX-DR23: `_keep_from` with a query and a fragment keeps `#` last."""
    from wedding.rsvp.views import _keep_from

    request = rf.get("/x/svar/dager/?fra=se-over")
    assert _keep_from(request, "/x/svar/dager/#velg-dager", "feil=1") == (
        "/x/svar/dager/?feil=1&fra=se-over#velg-dager"
    )


def test_summary_imports_first_in_a_fresh_interpreter():
    """No circular import: `wedding.rsvp.summary` loads before `forms`."""
    import subprocess
    import sys

    code = (
        "import django, os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings');"
        " django.setup(); import wedding.rsvp.summary"
    )
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_days_lines_for_mixed_days(client, seeded):
    """FR-14, FR-21: per-person day lines, chosen days by weekday and date; no
    overnight line for Filippa, who cannot stay."""
    arild, marie, _, _ = _arild_to_hike(client)
    client.post(_url(ARILD, "fjelltur"), {f"hike_{arild}": "yes", f"hike_{marie}": "maybe"})
    html = client.get(_url(ARILD, "se-over")).content.decode()
    blocks = [page_text(block) for block in _blocks(html)]
    assert "Arild: kommer Marie: kommer Filippa: kommer Leone: kommer ikke" in blocks[0]
    assert "Arild: hele helgen Marie: hele helgen Filippa: lørdag 27. mai" in blocks[1]
    assert "Arild: overnatter ikke Marie: overnatter ikke" in blocks[2]
    assert "Filippa" not in blocks[2]
    assert "Filippa" not in blocks[3]


def test_each_endre_link(client, seeded):
    """UX-DR23 (AC): each «Endre» goes to its step with `?fra=se-over`, with hidden
    context («Endre måltider»)."""
    _sigmund_to_check(client)
    html = client.get(_url(SIGMUND, "se-over")).content.decode()
    found = re.findall(
        r'<a class="check-list__change"\s+href="([^"]+)">Endre<span class="visually-hidden"> '
        r"([^<]+)</span></a>",
        html,
    )
    assert found == [
        (f"{_url(SIGMUND)}{FROM}", "hvem som kommer"),
        (f"{_url(SIGMUND, 'dager')}{FROM}", "dager"),
        (f"{_url(SIGMUND, 'overnatting')}{FROM}", "overnatting"),
        (f"{_url(SIGMUND, 'maltider')}{FROM}", "måltider"),
        (f"{_url(SIGMUND, 'allergier')}{FROM}", "allergier og matbehov"),
        (f"{_url(SIGMUND, 'fjelltur')}{FROM}", "fjelltur fredag"),
    ]


@pytest.mark.parametrize(
    ("slug", "data"),
    [
        ("", lambda s, b: {f"attendance_{s}": "yes", f"attendance_{b}": "yes"}),
        ("dager", lambda s, b: {"whole": "yes"}),
        ("overnatting", lambda s, b: {f"overnight_{s}": "yes", f"overnight_{b}": "yes"}),
        ("maltider", lambda s, b: {"action": "continue"}),
        ("allergier", lambda s, b: {f"allergies_{b}": "lactose"}),
        ("fjelltur", lambda s, b: {f"hike_{s}": "maybe", f"hike_{b}": "no"}),
    ],
)
def test_fortsett_from_endre_returns_to_the_check_page(client, seeded, slug, data):
    """UX-DR23, AD-7 (AC), matrix «Endre, no change» and «Endre, Tilbake»: the step
    opened with `fra` links «Tilbake» to the check page, and «Fortsett» returns."""
    sigmund, bestemor = _sigmund_to_check(client)
    url = f"{_url(SIGMUND, slug)}{FROM}"
    html = client.get(url).content.decode()
    assert f'href="{_url(SIGMUND, "se-over")}">Tilbake</a>' in html
    response = client.post(url, data(sigmund, bestemor))
    assert response.status_code == 302
    assert response["Location"] == _url(SIGMUND, "se-over")
    assert client.get(response["Location"]).status_code == 200


def test_endre_meals_adds_a_meal_and_raises_the_total(client, seeded):
    """MT-36 c): «Frokost søndag» for bestemor from the check page."""
    _, bestemor = _sigmund_to_check(client)
    response = client.post(
        f"{_url(SIGMUND, 'maltider')}{FROM}", {f"meals_{bestemor}": "sunday_breakfast"}
    )
    assert response["Location"] == _url(SIGMUND, "se-over")
    text = page_text(client.get(_url(SIGMUND, "se-over")).content.decode())
    assert "bestemor: frokost søndag" in text
    assert "Totalt for husstanden: 3 260 kr" in text


def test_endre_with_an_error_keeps_fra(client, seeded):
    """FR-22, UX-DR23, matrix «Endre, error»: an invalid post keeps `fra`, and
    fixing it returns to the check page."""
    sigmund, bestemor = _sigmund_to_check(client)
    response = client.post(f"{_url(SIGMUND)}{FROM}", {f"attendance_{sigmund}": "yes"})
    assert response.status_code == 303
    assert response["Location"] == f"{_url(SIGMUND)}?feil=1&fra=se-over"
    html = client.get(response["Location"]).content.decode()
    assert f'href="{_url(SIGMUND, "se-over")}">Tilbake</a>' in html
    response = client.post(
        response["Location"], {f"attendance_{sigmund}": "yes", f"attendance_{bestemor}": "yes"}
    )
    assert response["Location"] == _url(SIGMUND, "se-over")


def test_endre_keeps_fra_on_velg_and_the_day_groups(client, seeded):
    """UX-DR23: «Velg» and step 2's «Nei» reveal keep `fra`, before `#velg-dager`."""
    _, bestemor = _sigmund_to_check(client)
    response = client.post(
        f"{_url(SIGMUND, 'dager')}{FROM}", {"action": "switch", "respondent": str(bestemor)}
    )
    assert response["Location"] == f"{_url(SIGMUND, 'dager')}{FROM}"
    response = client.post(f"{_url(SIGMUND, 'dager')}{FROM}", {"whole": "no"})
    assert response["Location"] == f"{_url(SIGMUND, 'dager')}{FROM}#velg-dager"
    response = client.post(f"{_url(SIGMUND, 'dager')}{FROM}", {"whole": "no", "days_0": "fri"})
    assert response["Location"] == f"{_url(SIGMUND, 'dager')}?feil=1&fra=se-over"


def test_without_fra_fortsett_goes_to_the_next_step(client, seeded):
    """AD-7: «Tilbake» and «Fortsett» without `fra` go step by step as before."""
    sigmund, bestemor = _sigmund_to_check(client)
    response = client.post(
        _url(SIGMUND, "overnatting"),
        {f"overnight_{sigmund}": "yes", f"overnight_{bestemor}": "yes"},
    )
    assert response["Location"] == _url(SIGMUND, "maltider")
    response = client.post(f"{_url(SIGMUND, 'maltider')}?fra=noe-annet", {"action": "continue"})
    assert response["Location"] == _url(SIGMUND, "allergier")


def test_endre_adding_a_day_goes_through_the_new_questions(client, seeded):
    """AD-7, FR-75 (AC), matrix «Endre adds a day»: Filippa all days from «Endre
    dager» lands on step 3, then the steps in order, then the check page with a
    Fjelltur line for her once answered."""
    arild, marie, filippa, _ = _arild_to_hike(client)
    client.post(_url(ARILD, "fjelltur"), {f"hike_{arild}": "yes", f"hike_{marie}": "no"})
    response = client.post(
        f"{_url(ARILD, 'dager')}{FROM}",
        {
            "whole": "no",
            f"days_{arild}": ["fri", "sat", "sun"],
            f"days_{marie}": ["fri", "sat", "sun"],
            f"days_{filippa}": ["fri", "sat", "sun"],
        },
        follow=True,
    )
    assert response.redirect_chain[-1][0] == _url(ARILD, "overnatting")
    client.post(
        _url(ARILD, "overnatting"),
        {f"overnight_{arild}": "no", f"overnight_{marie}": "no", f"overnight_{filippa}": "no"},
    )
    client.post(_url(ARILD, "maltider"), {"action": "continue"})
    assert client.post(_url(ARILD, "allergier"), {"action": "continue"})["Location"] == _url(
        ARILD, "fjelltur"
    )
    html = client.get(_url(ARILD, "fjelltur")).content.decode()
    assert checked_radios(html)[f"hike_{arild}"] == "yes"
    assert f"hike_{filippa}" not in checked_radios(html)
    response = client.post(
        _url(ARILD, "fjelltur"),
        {f"hike_{arild}": "yes", f"hike_{marie}": "no", f"hike_{filippa}": "maybe"},
    )
    assert response["Location"] == _url(ARILD, "se-over")
    hike = page_text(_blocks(client.get(_url(ARILD, "se-over")).content.decode())[-1])
    assert "Filippa: kanskje" in hike


def test_a_post_without_send_writes_nothing(client, seeded):
    """AD-7 (Story 2.6a, matrix «No action»): a check-page POST without
    `action=send` redirects (303) back, with no draft change and no row."""
    _sigmund_to_check(client)
    before = row_counts()
    response = client.post(_url(SIGMUND, "se-over"), {})
    assert response.status_code == 303
    assert response["Location"] == _url(SIGMUND, "se-over")
    assert COOKIE_NAME not in response.cookies
    assert row_counts() == before


def test_the_walk_writes_nothing_and_is_never_cached(client, seeded):
    """AD-1, AD-8, FR-3: steps 1 to 6 and the check page, before the send, write no row, use no
    session and no messages, and every response is private and never stored."""
    before = row_counts()
    sigmund, bestemor = _ids(SIGMUND)
    requests = [
        ("post", _url(SIGMUND), {f"attendance_{sigmund}": "yes", f"attendance_{bestemor}": "yes"}),
        ("post", _url(SIGMUND, "dager"), {"whole": "yes"}),
        (
            "post",
            _url(SIGMUND, "overnatting"),
            {f"overnight_{sigmund}": "no", f"overnight_{bestemor}": "no"},
        ),
        ("post", _url(SIGMUND, "maltider"), {"action": "continue"}),
        ("post", _url(SIGMUND, "allergier"), {"action": "continue"}),
        ("get", _url(SIGMUND, "fjelltur"), {}),
        ("post", _url(SIGMUND, "fjelltur"), {f"hike_{sigmund}": "yes"}),
        ("get", f"{_url(SIGMUND, 'fjelltur')}?feil=1", {}),
        ("post", _url(SIGMUND, "fjelltur"), {f"hike_{sigmund}": "yes", f"hike_{bestemor}": "no"}),
        ("get", _url(SIGMUND, "se-over"), {}),
        ("get", f"{_url(SIGMUND, 'maltider')}{FROM}", {}),
        ("post", _url(SIGMUND, "se-over"), {}),
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
