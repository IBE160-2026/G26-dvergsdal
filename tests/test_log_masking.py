"""Link codes never reach the logs (Story 1.4c, FR-4, NFR-4, AD-15).

The log rows of the story's I/O matrix: `mask_link_codes` on Django's 404,
CSRF and development-server lines and on the paths that stay readable; every
handler in `LOGGING` carries the filter and none mails; and end to end, the
configured handlers' output after a 404, a CSRF failure and a server line
holds `/[code]/` and never the code. What the terminal shows is MT-9 in
docs/manual-test-plan.md.
"""

import logging
import tomllib
from io import StringIO
from pathlib import Path

import pytest
from django.core.management import call_command
from django.test import Client

from config.logging_filters import NOT_LINK_CODES, MaskLinkCodes, mask_link_codes

SEED_FILE = Path(__file__).resolve().parent.parent / "wedding" / "fixtures" / "seed.toml"
SEED = tomllib.loads(SEED_FILE.read_text(encoding="utf-8"))
CODE = SEED["households"][0]["guests"][0]["code"]
SERVER_LINE = '"%s" %s %s'


@pytest.mark.parametrize(
    ("message", "masked"),
    [
        (f"Not Found: /{CODE}/", "Not Found: /[code]/"),
        (
            f"Forbidden (CSRF cookie not set.): /{CODE}/",
            "Forbidden (CSRF cookie not set.): /[code]/",
        ),
        (f'"GET /{CODE}/svar/?x=1 HTTP/1.1" 404 0', '"GET /[code]/svar/?x=1 HTTP/1.1" 404 0'),
        (f"/{CODE}", "/[code]"),
        (f"('/{CODE}/',)", "('/[code]/',)"),
        ("Not Found: /hei/", "Not Found: /[code]/"),  # a mistyped code is masked too
        ("Not Found: /favicon.ico", "Not Found: /[code]"),
    ],
)
def test_first_path_segment_is_masked(message, masked):
    """NFR-4, AD-15: the first segment of a request path becomes `[code]`, whatever
    its length; the rest of the path and the query stay readable."""
    assert mask_link_codes(message) == masked


@pytest.mark.parametrize(
    "message",
    [
        "/",
        '"GET / HTTP/1.1" 200 1234',
        "/static/css/site.css",
        '"GET /static/img/forhandsvisning.jpg HTTP/1.1" 200 79719',
        "/stil/",
        "/robots.txt",
        "HTTP/1.1",
        "Starting development server at http://127.0.0.1:8000/",
    ],
)
def test_fixed_paths_are_left_alone(message):
    """NFR-4: `/`, static files, the style sample, robots.txt and `HTTP/1.1` are not
    link codes, so they stay readable."""
    assert mask_link_codes(message) == message


def test_not_link_codes_are_the_planned_ones():
    """AD-15: only these first segments are spared; Story 3.1 adds `admin`."""
    assert frozenset({"static", "stil", "robots.txt"}) == NOT_LINK_CODES


def test_filter_formats_masks_and_keeps_the_record():
    """AD-15: the filter formats the message with its arguments, masks it, leaves
    no arguments behind and never drops the record."""
    record = logging.LogRecord(
        "django.request", logging.WARNING, __file__, 1, "Not Found: %s", (f"/{CODE}/",), None
    )
    assert MaskLinkCodes().filter(record) is True
    assert record.msg == "Not Found: /[code]/"
    assert record.args == ()
    assert record.getMessage() == "Not Found: /[code]/"


def test_every_handler_masks_and_none_sends_mail(settings):
    """NFR-4, AD-15: every handler in LOGGING carries `mask_link_codes`, and there is
    no `mail_admins` handler, whose mail would carry the whole request."""
    logging_config = settings.LOGGING
    assert logging_config["filters"]["mask_link_codes"] == {
        "()": "config.logging_filters.MaskLinkCodes"
    }
    for name, handler in logging_config["handlers"].items():
        assert "mask_link_codes" in handler["filters"], name
        assert handler["class"] != "django.utils.log.AdminEmailHandler", name
    assert "mail_admins" not in logging_config["handlers"]
    assert logging_config["loggers"]["django"]["handlers"] == ["console"]


@pytest.fixture
def log_output():
    """Every handler LOGGING put on the `django` and `django.server` loggers writes
    to one StringIO for the length of the test; the old streams are put back after.
    (pytest adds handlers of its own, which are left alone.)"""
    output = StringIO()
    handlers = [
        handler
        for name in ("django", "django.server")
        for handler in logging.getLogger(name).handlers
        if handler.name in {"console", "django.server"}
    ]
    assert [handler.name for handler in handlers] == ["console", "django.server"]
    old_streams = [handler.setStream(output) for handler in handlers]
    try:
        yield output
    finally:
        for handler, stream in zip(handlers, old_streams, strict=True):
            handler.setStream(stream)


@pytest.mark.django_db
def test_configured_handlers_never_write_the_code(settings, monkeypatch, log_output):
    """FR-4, NFR-4, AD-15: with DEBUG on (as on the developer's machine), a 404 for a
    seeded link, a CSRF failure on it and a development-server line all reach the
    configured handlers with `/[code]/` and never the code."""
    monkeypatch.delenv("APP_ENV", raising=False)
    call_command("seed_testdata", stdout=StringIO())
    settings.DEBUG = True

    assert Client().get(f"/{CODE}/").status_code == 404
    response = Client(enforce_csrf_checks=True).post(f"/{CODE}/")
    assert response.status_code == 403
    logging.getLogger("django.server").info(SERVER_LINE, f"GET /{CODE}/svar/?x=1 HTTP/1.1", 404, 0)

    text = log_output.getvalue()
    assert CODE not in text
    assert "Not Found: /[code]/" in text
    assert "Forbidden (" in text
    assert "): /[code]/" in text
    assert '"GET /[code]/svar/?x=1 HTTP/1.1" 404 0' in text
