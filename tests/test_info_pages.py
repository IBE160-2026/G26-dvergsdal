"""The frame of the three info pages under `/<code>/` (Story 1.5, G3).

FR-5, FR-6, FR-8, FR-11, UX-DR11, UX-DR12. The info-page row of the story's
I/O matrix for `/program/`, `/praktisk/` and `/historie/`: the page's title and
`h1`, its nav word marked current and the others not, the back link and the
back button to the front page, the nav «Svar» to the front page's `#svar`, the
footer and two SELECTs. Unknown and malformed codes on each page show G1 with
404 after one and no query. The content of Praktisk informasjon and Vår
historie (Story 1.6) is tested in test_practical_and_story_pages.py, the
programme's (Story 1.7) in test_programme_page.py. That opening them never
writes is in test_front_page.py.
"""

import re

import pytest

from tests.helpers import page_text

CODE = "test-sigmund0000000000"
# Path -> (title, h1, the nav word marked current)
PAGES = {
    "program/": ("Programmet \N{EN DASH} Invitasjon", "Programmet", "Program"),
    "praktisk/": (
        "Praktisk informasjon \N{EN DASH} Invitasjon",
        "Praktisk informasjon",
        "Praktisk",
    ),
    "historie/": ("Vår historie \N{EN DASH} Invitasjon", "Vår historie", "Vår historie"),
}
NAV_WORDS = ("Program", "Praktisk", "Vår historie")

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("local_env")]


@pytest.mark.parametrize("path", PAGES)
def test_info_page_frame(
    client, seeded, django_assert_num_queries, assert_loads_only_own_host, path
):
    """FR-8, FR-11, UX-DR11: 200 after two SELECTs; the page's own title and one
    italic `h1`; its nav word current; back link at the top and back button at
    the bottom to the front page; nav «Svar» to the front page's `#svar`; the
    footer with the phones."""
    title, heading, current = PAGES[path]
    with django_assert_num_queries(2):
        response = client.get(f"/{CODE}/{path}")
    assert response.status_code == 200
    html = response.content.decode()
    assert f"<title>{title}</title>" in html
    assert html.count("<h1") == 1
    h1 = re.search(r'<h1 class="info-page__title"[^>]*>(.*?)</h1>', html, re.DOTALL).group(1)
    assert " ".join(h1.split()) == heading

    nav = html[html.index("<nav") : html.index("</nav>")]
    for word in NAV_WORDS:
        tag = re.search(rf"<a [^>]*>{word}</a>", nav).group(0)
        assert ('aria-current="page"' in tag) == (word == current), word
    assert re.search(rf'<a class="nav-bar__svar"\s+href="/{CODE}/#svar">Svar</a>', nav)

    main = html[html.index("<main") : html.index("</main>")]
    back = re.findall(rf'href="/{CODE}/">(.*?)</a>', main, re.DOTALL)
    assert [page_text(link) for link in back] == [
        "← Tilbake til invitasjonen",
        "Tilbake til invitasjonen",
    ]
    assert '<span aria-hidden="true">←</span> Tilbake til invitasjonen' in main
    assert re.search(r'<a class="button button--on-green"\s+href="/[^"]+/">', main)
    assert main.index("info-page__back") < main.index("<h1") < main.index("info-page__bottom")

    assert "<footer" in html
    assert 'href="tel:+4700000101"' in html
    assert "<script" not in html
    assert_loads_only_own_host(html)


@pytest.mark.parametrize("path", PAGES)
@pytest.mark.parametrize(("code", "queries"), [("AAAAAAAAAAAAAAAAAAAAAA", 1), ("hei", 0)])
def test_unknown_code_on_an_info_page_shows_g1_with_404(
    client, django_assert_num_queries, path, code, queries
):
    """FR-5, AD-6: an unknown code under an info page gives the same G1 body as `/`
    with 404, after one lookup for a well-formed code and none for a malformed one."""
    bare = client.get("/").content.decode()
    with django_assert_num_queries(queries):
        response = client.get(f"/{code}/{path}")
    assert response.status_code == 404
    assert response.content.decode() == bare
    assert "guests/private_invitation.html" in [template.name for template in response.templates]
