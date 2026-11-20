"""Helpers and constants shared by several test modules (Story 1.5).

Fixtures live in conftest.py; plain values and functions that tests import live
here.
"""

import re

# NFR-7, UX-DR4: the nine images the front page shows (Story 1.4b plans them,
# test_images.py keeps them within their budget, test_front_page.py checks that
# the rendered page shows exactly these).
FRONT_PAGE = (
    "segl.png",
    "illustrasjon.jpg",
    "brudeslor.png",
    "lilje-topp.png",
    "lilje-bunn.png",
    "blonde.png",
    "sted-middag.jpg",
    "sted-tunet.jpg",
    "oss-strand.jpg",
)


def page_text(html: str) -> str:
    """A page's text as a reader sees it: tags removed, whitespace collapsed."""
    return " ".join(re.sub(r"<[^>]+>", " ", html).split())
