"""Overnight stay, meals and the running total: steps 3 and 4 (Story 2.3).

FR-15, FR-16, FR-22, FR-32, FR-33, FR-70, FR-73, FR-75, AD-1, AD-7, AD-8,
AD-12, NFR-2, UX-DR16, UX-DR17, UX-DR19, UX-DR52. Every row of the story's
I/O matrix over HTTP, «Velg» on steps 3 and 4, Enter as «Fortsett», the one
script on the paid steps, the empty status region, `POST <base>/sum/`, and a
flow that writes no row, uses no session and is never cached. The rules are
in test_answer_rules.py; the browser runs are MT-30 to MT-32 in
docs/manual-test-plan.md.
"""

import datetime
import re

import pytest
from django.contrib.sessions.models import Session
from django.core import signing
from django.db import connection
from django.test import Client
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

from tests.helpers import checked_radios, page_text, row_counts, ticked_boxes
from wedding.models import Guest, Settings
from wedding.rsvp.draft import COOKIE_NAME, SALT

SIGMUND = "test-sigmund0000000000"
ARILD = "test-arild000000000000"
SYNNE = "test-synne000000000000"
EVA = "test-eva00000000000000"
ALL = ["fri", "sat", "sun"]
NBSP = "\N{NO-BREAK SPACE}"
DASH = "\N{EN DASH}"
MEALS = ["friday_dinner", "saturday_breakfast", "sunday_breakfast"]

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


def _ids(code: str) -> list[int]:
    household = Guest.objects.get(code=code).household
    return list(household.guests.order_by("id").values_list("id", flat=True))


def _url(code: str, slug: str = "") -> str:
    return f"/{code}/svar/{slug}/" if slug else f"/{code}/svar/"


def _answers(code: str, *coming: bool) -> dict[str, str]:
    return {
        f"attendance_{guest_id}": "yes" if answer else "no"
        for guest_id, answer in zip(_ids(code), coming, strict=True)
    }


def _draft(response) -> dict:
    return signing.loads(response.cookies[COOKIE_NAME].value, salt=SALT)


def _total(html: str) -> str:
    match = re.search(
        r'<p class="form-total">Totalt for husstanden: <strong>(.*?)</strong></p>', html
    )
    return match.group(1).replace(NBSP, " ")


def _links(html: str) -> list[tuple[str, str]]:
    return re.findall(r'<li>\s*<a href="(#[^"]+)">([^<]+)</a>\s*</li>', html)


def _groups(html: str) -> list[str]:
    return re.findall(r"<fieldset\b[^>]*>.*?</fieldset>", html, re.DOTALL)[1:]


def _legend(group: str) -> str:
    return re.search(r"<legend>(.*?)</legend>", group).group(1)


def _sigmund_to_overnight(client) -> None:
    client.post(_url(SIGMUND), _answers(SIGMUND, True, True))
    response = client.post(_url(SIGMUND, "dager"), {"whole": "yes"})
    assert response["Location"] == _url(SIGMUND, "overnatting")


def _both_stay(client):
    sigmund, bestemor = _ids(SIGMUND)
    _sigmund_to_overnight(client)
    return client.post(
        _url(SIGMUND, "overnatting"),
        {f"overnight_{sigmund}": "yes", f"overnight_{bestemor}": "yes"},
    )


def _arild_to_overnight(client, filippa_days: list[str]) -> None:
    """Arild, Marie and Filippa «Kommer», Leone not; «Nei», all days but Filippa's."""
    arild, marie, filippa, _ = _ids(ARILD)
    client.post(_url(ARILD), _answers(ARILD, True, True, True, False))
    client.post(_url(ARILD, "dager"), {"whole": "no"})
    response = client.post(
        _url(ARILD, "dager"),
        {
            "whole": "no",
            f"days_{arild}": ALL,
            f"days_{marie}": ALL,
            f"days_{filippa}": filippa_days,
        },
    )
    assert response["Location"] == _url(ARILD, "overnatting")


def _arild_done(client) -> None:
    """Steps 1 to 4 for Arild's household; Filippa Saturday + Sunday, staying, with
    Sunday breakfast."""
    arild, marie, filippa, _ = _ids(ARILD)
    _arild_to_overnight(client, ["sat", "sun"])
    client.post(
        _url(ARILD, "overnatting"),
        {f"overnight_{arild}": "yes", f"overnight_{marie}": "yes", f"overnight_{filippa}": "yes"},
    )
    response = client.post(_url(ARILD, "maltider"), {f"meals_{filippa}": "sunday_breakfast"})
    assert response["Location"] == _url(ARILD, "allergier")


# The I/O matrix


def test_open_overnight(client, seeded, django_assert_num_queries):
    """FR-16, FR-32, FR-33: «Steg 3 av 6», a group per person, the price per person,
    why guests pay, a total of 0 kr, one script and an empty status region."""
    _sigmund_to_overnight(client)
    with django_assert_num_queries(4):
        response = client.get(_url(SIGMUND, "overnatting"))
    html = response.content.decode()
    text = page_text(html)
    assert '<h1 id="sporsmal">Hvem skal overnatte på Hardingasete?</h1>' in html
    assert '<p class="form-progress">Steg 3 av 6: Overnatting</p>' in html
    assert [_legend(group) for group in _groups(html)] == ["Sigmund", "bestemor"]
    assert f"Hytte hele helgen: <b>1{NBSP}500{NBSP}kr</b> per person" in html
    assert (
        "Hyttene er leid for hele helgen, fra fredag 26. mai til søndag 28. mai. Begge nettene "
        "betales, også for den som bare sover der én natt." in text
    )
    assert (
        "Dette er Hardingasetes priser, og hver gjest betaler selv. Lunsj og middag på "
        "bryllupsdagen dekker vi." in text
    )
    assert f"Ja, hytte hele helgen {DASH} 1 500 kr" in text
    assert _total(html) == "0 kr"
    assert html.count("<script") == 1
    assert re.search(r'<script src="/static/js/rsvp-total\.js" defer></script>', html)
    assert '<p class="visually-hidden" role="status" id="total-status"></p>' in html
    assert f'data-total-url="{_url(SIGMUND, "sum")}?steg=overnatting"' in html
    assert {k for k in checked_radios(html) if k.startswith("overnight_")} == set()
    assert f'href="{_url(SIGMUND, "dager")}">Tilbake</a>' in html


def test_both_stay(client, seeded):
    """FR-16, FR-33: both «Ja» goes to meals, where the total is 3 000 kr and each has
    all three meals."""
    response = _both_stay(client)
    assert response.status_code == 302
    assert response["Location"] == _url(SIGMUND, "maltider")
    assert "overnight" in _draft(response)["done"]
    html = client.get(response["Location"]).content.decode()
    assert '<h1 id="sporsmal">Hvilke måltider skal vi bestille?</h1>' in html
    assert _total(html) == "3 000 kr"
    groups = _groups(html)
    assert [group.count('type="checkbox"') for group in groups] == [3, 3]
    text = page_text(html)
    for label in (
        f"Middag fredag {DASH} 340 kr",
        f"Frokost lørdag {DASH} 260 kr",
        f"Frokost søndag {DASH} 260 kr",
    ):
        assert label in text
    assert "Kryss av for måltidene hver person skal ha. Det er greit å ikke velge noen." in text
    assert "Lunsj" not in page_text("".join(groups))
    assert html.count("<script") == 1


def test_missing(client, seeded):
    """FR-22: only Sigmund «Ja»: 303 to `?feil=1`, one link for bestemor, Sigmund's
    «Ja» kept, total 1 500 kr."""
    sigmund, bestemor = _ids(SIGMUND)
    _sigmund_to_overnight(client)
    response = client.post(_url(SIGMUND, "overnatting"), {f"overnight_{sigmund}": "yes"})
    assert response.status_code == 303
    assert response["Location"] == f"{_url(SIGMUND, 'overnatting')}?feil=1"
    assert "overnight" not in _draft(response)["done"]
    html = client.get(response["Location"]).content.decode()
    assert _links(html) == [(f"#overnight_{bestemor}_yes", "Velg overnatting for bestemor")]
    assert "Feil: Velg «Ja» eller «Nei» for bestemor." in page_text(html)
    assert checked_radios(html)[f"overnight_{sigmund}"] == "yes"
    assert _total(html) == "1 500 kr"
    assert html.startswith("\n<!DOCTYPE") or "<title>Feil: " in html


def test_one_day_is_blocked(client, seeded):
    """FR-70: Filippa on Saturday only, «Ja»: refused with the reason under her
    legend, and nothing chosen for her."""
    arild, marie, filippa, _ = _ids(ARILD)
    _arild_to_overnight(client, ["sat"])
    response = client.post(
        _url(ARILD, "overnatting"),
        {f"overnight_{arild}": "no", f"overnight_{marie}": "no", f"overnight_{filippa}": "yes"},
    )
    assert response.status_code == 303
    assert _draft(response)["night"] == {str(arild): False, str(marie): False}
    html = client.get(response["Location"]).content.decode()
    group = _groups(html)[2]
    assert _legend(group) == "Filippa"
    assert (
        "Feil: For å overnatte må man være med minst to dager på rad, og Filippa kommer bare "
        "lørdag. Velg «Nei», eller gå tilbake og velg flere dager for Filippa." in page_text(group)
    )
    assert f"overnight_{filippa}" not in checked_radios(html)
    assert _links(html) == [(f"#overnight_{filippa}_yes", "Velg overnatting for Filippa")]


def test_meals(client, seeded):
    """FR-15, FR-33: Sigmund all three, bestemor Sunday breakfast plus a forged key:
    on to allergies, total 3 000 + 860 + 260 = 4 120 kr."""
    sigmund, bestemor = _ids(SIGMUND)
    _both_stay(client)
    response = client.post(
        _url(SIGMUND, "maltider"),
        {f"meals_{sigmund}": MEALS, f"meals_{bestemor}": ["sunday_breakfast", "lunch"]},
    )
    assert response.status_code == 302
    assert response["Location"] == _url(SIGMUND, "allergier")
    draft = _draft(response)
    assert draft["meals"] == {str(sigmund): MEALS, str(bestemor): ["sunday_breakfast"]}
    assert "meals" in draft["done"]
    html = client.get(_url(SIGMUND, "maltider")).content.decode()
    assert _total(html) == "4 120 kr"
    assert len(ticked_boxes(html)) == 4


def test_filippa_meals(client, seeded):
    """FR-73: Filippa on Saturday and Sunday is offered only Sunday breakfast."""
    _arild_done(client)
    html = client.get(_url(ARILD, "maltider")).content.decode()
    group = _groups(html)[2]
    assert _legend(group) == "Filippa"
    assert group.count('type="checkbox"') == 1
    assert f"Frokost søndag {DASH} 260 kr" in page_text(group)
    assert _total(html) == "4 760 kr"  # three cabins and one breakfast


def test_no_meals_for_synne(client, seeded):
    """FR-17, FR-73: Synne on Saturday only skips steps 3 and 4."""
    synne = _ids(SYNNE)[0]
    client.post(_url(SYNNE), _answers(SYNNE, True))
    client.post(_url(SYNNE, "dager"), {"whole": "no"})
    response = client.post(_url(SYNNE, "dager"), {"whole": "no", f"days_{synne}": "sat"})
    assert response["Location"] == _url(SYNNE, "allergier")
    assert client.get(_url(SYNNE, "maltider"))["Location"] == _url(SYNNE, "allergier")


def test_a_removed_day_reopens_the_later_steps(client, seeded):
    """FR-75: Filippa down to Saturday after step 4: her stay and meal are gone, the
    steps after step 2 are not done, and the check page goes to step 3."""
    arild, marie, filippa, _ = _ids(ARILD)
    _arild_done(client)
    response = client.post(
        _url(ARILD, "dager"),
        {"whole": "no", f"days_{arild}": ALL, f"days_{marie}": ALL, f"days_{filippa}": "sat"},
    )
    draft = _draft(response)
    assert str(filippa) not in draft["night"]
    assert str(filippa) not in draft["meals"]
    assert draft["done"] == ["who", "days"]
    assert client.get(_url(ARILD, "se-over"))["Location"] == _url(ARILD, "overnatting")


def test_someone_who_stops_coming_reopens_the_later_steps(client, seeded):
    """FR-75: bestemor «Kommer ikke» after step 4: her stay and meals are removed and
    the later steps open again."""
    sigmund, bestemor = _ids(SIGMUND)
    _both_stay(client)
    client.post(_url(SIGMUND, "maltider"), {f"meals_{bestemor}": MEALS})
    response = client.post(_url(SIGMUND), _answers(SIGMUND, True, False))
    draft = _draft(response)
    assert draft["night"] == {str(sigmund): True}
    assert draft["meals"] == {}
    assert draft["done"] == ["who", "days"]


def test_the_same_presence_keeps_the_later_steps(client, seeded):
    """FR-75: step 2 posted again with the same days keeps overnight and meals done."""
    arild, marie, filippa, _ = _ids(ARILD)
    _arild_done(client)
    response = client.post(
        _url(ARILD, "dager"),
        {
            "whole": "no",
            f"days_{arild}": ALL,
            f"days_{marie}": ALL,
            f"days_{filippa}": ["sat", "sun"],
        },
    )
    assert _draft(response)["done"] == ["who", "days", "overnight", "meals"]


def test_a_price_of_zero(client, seeded):
    """FR-32 (Rikke 2026-11-21): a free cabin is offered with no price and no price line."""
    Settings.objects.update(price_cabin_weekend=0)
    _both_stay(client)
    html = client.get(_url(SIGMUND, "overnatting")).content.decode()
    assert "Ja, hytte hele helgen </label>" in re.sub(r"\s+", " ", html)
    assert "form-price" not in html
    assert _total(html) == "0 kr"


def test_sum(client, seeded, django_assert_num_queries):
    """AD-7, FR-33: the running total of the posted choices, no cookie, three SELECTs."""
    sigmund, bestemor = _ids(SIGMUND)
    _sigmund_to_overnight(client)
    with django_assert_num_queries(3):
        response = client.post(
            f"{_url(SIGMUND, 'sum')}?steg=overnatting",
            {f"overnight_{sigmund}": "yes", f"overnight_{bestemor}": "yes"},
        )
    assert response.status_code == 200
    assert _total(response.content.decode()) == "3 000 kr"
    assert not response.cookies
    assert "private" in response["Cache-Control"]
    assert "no-store" in response["Cache-Control"]


def test_sum_on_meals(client, seeded):
    """AD-7, FR-33: on step 4 the posted meals replace the saved ones."""
    sigmund, _ = _ids(SIGMUND)
    _both_stay(client)
    response = client.post(f"{_url(SIGMUND, 'sum')}?steg=maltider", {f"meals_{sigmund}": MEALS})
    assert _total(response.content.decode()) == "3 860 kr"


@pytest.mark.parametrize("steg", ["dager", "", "allergier"])
def test_sum_refuses_other_steps(client, seeded, steg):
    """AD-7: 204 for any step without prices."""
    _sigmund_to_overnight(client)
    response = client.post(f"{_url(SIGMUND, 'sum')}?steg={steg}")
    assert response.status_code == 204
    assert response.content == b""


def test_sum_refuses_without_a_draft(client, seeded):
    """AD-7, AD-8: no draft, a broken one or step 1 not done gives 204, and a broken
    cookie is not deleted."""
    url = f"{_url(SIGMUND, 'sum')}?steg=overnatting"
    assert client.post(url).status_code == 204
    client.cookies[COOKIE_NAME] = "broken"
    response = client.post(url)
    assert response.status_code == 204
    assert not response.cookies
    client.cookies.pop(COOKIE_NAME)
    client.post(_url(SIGMUND), {f"attendance_{_ids(SIGMUND)[0]}": "yes"})
    assert client.post(url).status_code == 204


def test_sum_after_the_deadline(client, seeded):
    """FR-41, AD-11: after the deadline the total is 204."""
    _sigmund_to_overnight(client)
    Settings.objects.update(rsvp_deadline=timezone.localdate() - datetime.timedelta(days=1))
    assert client.post(f"{_url(SIGMUND, 'sum')}?steg=overnatting").status_code == 204


def test_sum_is_post_only_and_unknown_codes_get_g1(client, seeded):
    """AD-7, FR-5: GET is refused; an unknown code is G1 with 404."""
    assert client.get(f"{_url(SIGMUND, 'sum')}?steg=overnatting").status_code == 405
    assert client.post("/AAAAAAAAAAAAAAAAAAAAAA/svar/sum/?steg=overnatting").status_code == 404


def test_broken_night_or_meals_start_empty(client, seeded):
    """AD-8: a non-bool stay is broken: deleted, step 1 empty, no 500."""
    ids = _ids(SIGMUND)
    payload = {
        "v": 3,
        "started": "2026-11-21T10:00:00+00:00",
        "rev": 0,
        "resp": ids[0],
        "att": {str(guest_id): True for guest_id in ids},
        "done": ["who"],
        "whole": True,
        "days": {},
        "night": {str(ids[0]): "yes"},
        "meals": {},
    }
    client.cookies[COOKIE_NAME] = signing.dumps(payload, salt=SALT, compress=True)
    response = client.get(_url(SIGMUND))
    assert response.status_code == 200
    assert response.cookies[COOKIE_NAME]["max-age"] == 0


def test_csrf(seeded):
    """UX-DR52, FR-33: bestemor «Ja» posted without a token: 403, her «Ja» checked,
    the total includes it, no draft written."""
    _, bestemor = _ids(SIGMUND)
    client = Client()
    _sigmund_to_overnight(client)
    client.handler.enforce_csrf_checks = True
    response = client.post(_url(SIGMUND, "overnatting"), {f"overnight_{bestemor}": "yes"})
    assert response.status_code == 403
    html = response.content.decode()
    assert checked_radios(html)[f"overnight_{bestemor}"] == "yes"
    assert _total(html) == "1 500 kr"
    assert COOKIE_NAME not in response.cookies
    assert "Prøv igjen." in page_text(html)


def test_csrf_on_meals(seeded):
    """UX-DR52: the posted meals are ticked and counted."""
    sigmund, _ = _ids(SIGMUND)
    client = Client()
    _both_stay(client)
    client.handler.enforce_csrf_checks = True
    response = client.post(_url(SIGMUND, "maltider"), {f"meals_{sigmund}": "friday_dinner"})
    assert response.status_code == 403
    html = response.content.decode()
    assert ticked_boxes(html) == [f"meals_{sigmund}_friday_dinner"]
    assert _total(html) == "3 340 kr"


# «Velg», Enter and the flow


@pytest.mark.parametrize("step", ["overnatting", "maltider"])
def test_velg_keeps_the_choices(client, seeded, step):
    """FR-12, UX-DR18: «Velg» keeps the respondent and the posted choices without
    validating or marking the step done."""
    sigmund, bestemor = _ids(SIGMUND)
    _both_stay(client) if step == "maltider" else _sigmund_to_overnight(client)
    field = f"overnight_{sigmund}" if step == "overnatting" else f"meals_{sigmund}"
    value = "yes" if step == "overnatting" else "friday_dinner"
    response = client.post(
        _url(SIGMUND, step), {"action": "switch", "respondent": str(bestemor), field: value}
    )
    assert response["Location"] == _url(SIGMUND, step)
    draft = _draft(response)
    assert draft["resp"] == bestemor
    if step == "overnatting":
        assert draft["night"] == {str(sigmund): True}
        assert "overnight" not in draft["done"]
    else:
        assert draft["meals"] == {str(sigmund): ["friday_dinner"]}
        assert "meals" not in draft["done"]


@pytest.mark.parametrize("step", ["overnatting", "maltider"])
def test_enter_submits_as_fortsett(client, seeded, step):
    """UX-DR18: the first button in the form is the hidden «Fortsett»."""
    _both_stay(client)
    html = client.get(_url(SIGMUND, step)).content.decode()
    form = html[html.index("<form") :]
    first = re.search(r"<button[^>]*>[^<]*</button>", form).group(0)
    assert first == '<button type="submit" hidden>Fortsett</button>'


def test_the_flow_writes_nothing_and_is_never_cached(client, seeded):
    """AD-1, AD-8, FR-3, FR-33: steps 1 to 4 and the total: no row, no session,
    four SELECTs per form request (Story 2.8 adds the answer check), three for
    the total, private and never stored; scripts only on steps 3
    and 4 and the allergies script on step 5; the shown total is always
    `household_total` of the draft."""
    sigmund, bestemor = _ids(SIGMUND)
    over, meals = _url(SIGMUND, "overnatting"), _url(SIGMUND, "maltider")
    before = row_counts()
    requests = [
        ("get", _url(SIGMUND), {}, 200, None),
        ("post", _url(SIGMUND), _answers(SIGMUND, True, True), 302, None),
        ("get", _url(SIGMUND, "dager"), {}, 200, None),
        ("post", _url(SIGMUND, "dager"), {"whole": "yes"}, 302, None),
        ("get", over, {}, 200, "0 kr"),
        (
            "post",
            f"{_url(SIGMUND, 'sum')}?steg=overnatting",
            {f"overnight_{sigmund}": "yes"},
            200,
            "1 500 kr",
        ),
        ("post", over, {f"overnight_{sigmund}": "yes"}, 303, None),
        ("get", f"{over}?feil=1", {}, 200, "1 500 kr"),
        ("post", over, {f"overnight_{sigmund}": "yes", f"overnight_{bestemor}": "no"}, 302, None),
        ("get", meals, {}, 200, "1 500 kr"),
        ("post", meals, {f"meals_{bestemor}": MEALS}, 302, None),
        ("get", meals, {}, 200, "2 360 kr"),
        ("get", _url(SIGMUND, "allergier"), {}, 200, None),
    ]
    for method, path, data, status, total in requests:
        with CaptureQueriesContext(connection) as captured:
            response = getattr(client, method)(path, data)
        assert response.status_code == status, (method, path)
        sql = [query["sql"] for query in captured.captured_queries]
        assert len(sql) == (3 if "/sum/" in path else 4), (method, path, sql)
        assert all(statement.lstrip().upper().startswith("SELECT") for statement in sql)
        assert "private" in response["Cache-Control"]
        assert "no-store" in response["Cache-Control"]
        html = response.content.decode()
        paid = method == "get" and path.split("?")[0] in (over, meals)
        allergies = method == "get" and path == _url(SIGMUND, "allergier")
        assert html.count("<script") == (1 if paid or allergies else 0), path
        if total is not None:
            assert _total(html) == total, path
            assert f"{total.replace(' ', NBSP)}</strong>" in html
        assert "sessionid" not in response.cookies
    assert row_counts() == before
    assert Session.objects.count() == 0
