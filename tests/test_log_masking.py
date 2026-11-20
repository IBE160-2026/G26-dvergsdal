"""Link codes never reach the logs (Story 1.4c, FR-4, NFR-4, AD-15).

The log rows of the story's I/O matrix: `mask_link_codes` on Django's 404,
CSRF and development-server lines, on full URLs and on the paths that stay
readable; the filter on exception text and stacks; every handler in `LOGGING`
carries the filter first and none mails; and end to end, the configured
handlers' output after a 404, a seeded link's 200 (Story 1.5), a CSRF failure
and a server line (DEBUG on) and
after an error with DEBUG off holds `/[code]/` and never the code. That
`NOT_LINK_CODES` covers every fixed route is in test_guest_privacy.py. What the
terminal shows is MT-9 in docs/manual-test-plan.md.
"""

import logging
import sys
import tomllib
from io import StringIO
from pathlib import Path

import pytest
from django.core.management import call_command
from django.test import Client

from config.logging_filters import MaskLinkCodes, mask_link_codes

SEED_FILE = Path(__file__).resolve().parent.parent / "wedding" / "fixtures" / "seed.toml"
SEED = tomllib.loads(SEED_FILE.read_text(encoding="utf-8"))
CODE = SEED["households"][0]["guests"][0]["code"]
UNKNOWN_CODE = "AAAAAAAAAAAAAAAAAAAAAA"
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
        (f'"GET //{CODE}/ HTTP/1.1" 404 0', '"GET //[code]/ HTTP/1.1" 404 0'),
        (
            f"Forbidden (Referer checking failed - 'https://example.org/{CODE}/' does not "
            "match any trusted origins.): /x/",
            "Forbidden (Referer checking failed - 'https://example.org/[code]/' does not "
            "match any trusted origins.): /[code]/",
        ),
        (f"http://127.0.0.1:8000/{CODE}/svar/", "http://127.0.0.1:8000/[code]/svar/"),
        (f"Not Found: /x/?next=/{CODE}/", "Not Found: /[code]/?next=/[code]/"),
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
        "http://127.0.0.1:8000/static/css/site.css",
        "https://example.org/robots.txt",
    ],
)
def test_fixed_paths_are_left_alone(message):
    """NFR-4: `/`, a bare site address, static files, the style sample, robots.txt
    and `HTTP/1.1` are not link codes, so they stay readable."""
    assert mask_link_codes(message) == message


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


def test_filter_masks_the_traceback_and_the_stack():
    """AD-15: an exception whose text holds a code is formatted into `exc_text`,
    masked, and `exc_info` cleared, so no formatter prints it again unmasked; the
    stack is masked too."""
    try:
        raise ValueError(f"no guest for /{CODE}/")
    except ValueError:
        record = logging.getLogger("django.request").makeRecord(
            "django.request",
            logging.ERROR,
            __file__,
            1,
            "Internal Server Error: %s",
            (f"/{CODE}/",),
            sys.exc_info(),
            sinfo=f"Stack (most recent call last):\n  /{CODE}/",
        )
    assert MaskLinkCodes().filter(record) is True
    assert record.exc_info is None
    assert "ValueError: no guest for /[code]/" in record.exc_text
    assert record.stack_info.endswith("/[code]/")
    text = logging.Formatter().format(record)
    assert CODE not in text
    assert text.startswith("Internal Server Error: /[code]/")


def test_filter_passes_a_broken_record_on_unchanged():
    """AD-15: a record whose arguments do not fit its message is passed on as it is
    instead of raising inside the request."""
    record = logging.LogRecord("x", logging.WARNING, __file__, 1, "%s %s", ("one",), None)
    assert MaskLinkCodes().filter(record) is True
    assert record.msg == "%s %s"
    assert record.args == ("one",)


def test_every_handler_masks_first_and_none_sends_mail(settings):
    """NFR-4, AD-15: every handler in LOGGING, the root logger's too, carries
    `mask_link_codes` as its first filter, so no other filter can reject a record
    that then goes on unmasked; there is no `mail_admins` handler, whose mail would
    carry the whole request; and WARNING and above reach a handler whatever DEBUG
    is."""
    logging_config = settings.LOGGING
    assert logging_config["filters"]["mask_link_codes"] == {
        "()": "config.logging_filters.MaskLinkCodes"
    }
    for name, handler in logging_config["handlers"].items():
        assert handler["filters"][0] == "mask_link_codes", name
        assert handler["class"] != "django.utils.log.AdminEmailHandler", name
    assert "mail_admins" not in logging_config["handlers"]
    assert logging_config["root"] == {"handlers": ["errors"], "level": "WARNING"}
    errors = logging_config["handlers"]["errors"]
    assert errors["level"] == "WARNING"
    assert errors["filters"] == ["mask_link_codes"]  # no DEBUG filter
    assert logging_config["loggers"]["django"]["handlers"] == ["console"]
    configured = [
        handler
        for name in ("", "django", "django.server")
        for handler in logging.getLogger(name).handlers
        if handler.name in logging_config["handlers"]
    ]
    assert {handler.name for handler in configured} == set(logging_config["handlers"])
    for handler in configured:
        assert isinstance(handler.filters[0], MaskLinkCodes), handler.name


@pytest.fixture
def log_output():
    """Every handler LOGGING put on the root, `django` and `django.server` loggers
    writes to one StringIO for the length of the test; the old streams are put
    back after. (pytest adds handlers of its own, which are left alone.)"""
    output = StringIO()
    handlers = [
        handler
        for name in ("", "django", "django.server")
        for handler in logging.getLogger(name).handlers
        if handler.name in {"errors", "console", "django.server"}
    ]
    assert [handler.name for handler in handlers] == ["errors", "console", "django.server"]
    old_streams = [handler.setStream(output) for handler in handlers]
    try:
        yield output
    finally:
        for handler, stream in zip(handlers, old_streams, strict=True):
            handler.setStream(stream)


@pytest.mark.django_db
def test_configured_handlers_never_write_the_code(settings, monkeypatch, log_output):
    """FR-4, NFR-4, AD-15: with DEBUG on (as on the developer's machine), a 404 for an
    unknown code, a seeded link that opens the invitation, a CSRF failure on it and
    a development-server line all reach the configured handlers with `/[code]/`
    and never a code."""
    monkeypatch.delenv("APP_ENV", raising=False)
    call_command("seed_testdata", stdout=StringIO())
    settings.DEBUG = True

    assert Client().get(f"/{UNKNOWN_CODE}/").status_code == 404
    assert Client().get(f"/{CODE}/").status_code == 200
    response = Client(enforce_csrf_checks=True).post(f"/{CODE}/")
    assert response.status_code == 403
    logging.getLogger("django.server").info(SERVER_LINE, f"GET /{CODE}/svar/?x=1 HTTP/1.1", 404, 0)

    text = log_output.getvalue()
    assert CODE not in text
    assert UNKNOWN_CODE not in text
    assert text.count("Not Found: /[code]/") == 1  # never by both console and errors
    assert "Forbidden (" in text
    assert "): /[code]/" in text
    assert '"GET /[code]/svar/?x=1 HTTP/1.1" 404 0' in text


def test_with_debug_off_errors_still_reach_a_masked_handler(settings, log_output):
    """NFR-4, AD-15: with DEBUG off (production) the debug console stays quiet, but
    an error from Django and a warning from our own code still reach the `errors`
    handler, masked, instead of Python's unmasked last-resort handler."""
    settings.DEBUG = False
    logging.getLogger("django.request").error("Internal Server Error: %s", f"/{CODE}/")
    logging.getLogger("wedding").warning("Slow page: %s", f"/{CODE}/svar/")
    logging.getLogger("django.request").info("Only with DEBUG: %s", f"/{CODE}/")

    text = log_output.getvalue()
    assert CODE not in text
    assert "Internal Server Error: /[code]/" in text
    assert "Slow page: /[code]/svar/" in text
    assert "Only with DEBUG" not in text
