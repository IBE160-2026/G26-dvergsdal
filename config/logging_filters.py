"""Logging filters that keep link codes out of the logs (Story 1.4c, FR-4, NFR-4, AD-15).

A guest's link code is their only login, so a log line such as
«Not Found: /<code>/» or the development server's «"GET /<code>/ HTTP/1.1" 404»
would put a working login in the terminal and in any log file. `MaskLinkCodes`
sits first on every handler in `LOGGING` (config/settings.py) and rewrites the
first segment of every path in the message, the exception text and the stack
to `[code]`, and any bare 22-character code (Story 3.1 widened both).
`BelowWarning` keeps the debug-only console handler to INFO, since
the `errors` handler already writes WARNING and above.
"""

import logging
import re

# First path segments that are never link codes, so they stay readable in the
# log (Story 3.1 adds `admin`). Anything not listed here is masked: masking too
# much only makes a log line less helpful, masking too little leaks a login.
# tests/test_admin_routing.py checks that every reserved first segment of the
# root URLconf is listed.
NOT_LINK_CODES = frozenset({"static", "stil", "robots.txt", "admin"})

# `wedding.links.CODE_LENGTH`; a test keeps the two equal, as for `Guest.code`.
CODE_LENGTH = 22

# A path is one or more slashes (`/`, or `%2F` when the path sits percent-encoded
# in a query such as `?next=%2F<code>%2F`) either after `scheme://host` (a full
# URL, as in Django's CSRF «Referer checking failed - 'https://host/<code>/' …»)
# or at the start of the message or after whitespace, a quote, a bracket, `(`,
# `=`, `:`, `,`, `{`, `<`, `;` or `|` (`?next=/<code>/`, `[/<code>/]`,
# `path:/<code>/`). Its first segment runs to the next slash, space, query,
# fragment or quote. `HTTP/1.1` is not a path: its `/` follows a letter.
_SLASH = r"(?:/|%2[Ff])"
_PATH = re.compile(
    r"""(?:(?P<origin>\b[A-Za-z][\w+.-]*://[^/\s?#"']*)|(?<![^\s"'(=:,{<;|\[]))"""
    rf"""(?P<slashes>{_SLASH}+)(?P<segment>(?:(?!{_SLASH})[^\s?#"'])+)"""
)

# A link code with no slash around it («code=<code>», «{'path': '<code>/x/'}»):
# exactly CODE_LENGTH URL-safe characters, not part of a longer word, with an
# uppercase letter or a digit so an ordinary lower-case word is left alone.
_BARE_CODE = re.compile(
    rf"(?<![\w-])(?=[A-Za-z0-9_-]*[A-Z0-9])[A-Za-z0-9_-]{{{CODE_LENGTH}}}(?![\w-])"
)


def _mask(match: re.Match[str]) -> str:
    if match["segment"] in NOT_LINK_CODES:
        return match[0]
    before = match.string[match.start() - 1 : match.start()]
    if before == ":" and match["slashes"].startswith("//") and not match["origin"]:
        return match[0]  # the `//` of a `scheme://host` address, not a path
    return f"{match['origin'] or ''}{match['slashes']}[code]"


def mask_link_codes(message: str) -> str:
    """NFR-4, AD-15: `message` with every link code as `[code]`.

    Two passes. First the first segment of every path, whatever its length,
    because a mistyped code is nearly a real one, and whether the slashes are
    written `/` or `%2F` and follow a space, a bracket, a colon or similar. That
    includes the first folder of a file path (the autoreloader's «/home/user/…»
    becomes «/[code]/user/…»), which is harmless. Then any bare 22-character
    code with no slash around it. `/`, `http://127.0.0.1:8000/`, `HTTP/1.1` and
    paths under `NOT_LINK_CODES` (`/admin/logg-inn/?next=/admin/`) are left as
    they are.
    """
    return _BARE_CODE.sub("[code]", _PATH.sub(_mask, message))


class MaskLinkCodes(logging.Filter):
    """NFR-4, AD-15: masks link codes in every record a handler writes.

    The message is formatted first (`getMessage()`), because Django passes the
    path as an argument, then masked and stored back with no arguments left.
    A traceback is formatted into `exc_text` and masked, and `exc_info` cleared,
    so no formatter prints it again unmasked; `stack_info` is masked too. A
    record whose message cannot be formatted is passed on unchanged, so logging
    never breaks a request. It never drops a record.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            message = record.getMessage()
        except Exception:
            return True
        record.msg = mask_link_codes(message)
        record.args = ()
        if record.exc_info:
            record.exc_text = logging.Formatter().formatException(record.exc_info)
            record.exc_info = None
        if record.exc_text:
            record.exc_text = mask_link_codes(record.exc_text)
        if record.stack_info:
            record.stack_info = mask_link_codes(record.stack_info)
        return True


class BelowWarning(logging.Filter):
    """AD-15: passes only records below WARNING, so the debug console and the
    `errors` handler never print the same line twice."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno < logging.WARNING
