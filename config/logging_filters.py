"""Logging filter that keeps link codes out of the logs (Story 1.4c, FR-4, NFR-4, AD-15).

A guest's link code is their only login, so a log line such as
«Not Found: /<code>/» or the development server's «"GET /<code>/ HTTP/1.1" 404»
would put a working login in the terminal and in any log file. `MaskLinkCodes`
sits on every handler in `LOGGING` (config/settings.py) and rewrites the first
segment of every request path in the message to `[code]`.
"""

import logging
import re

# First path segments that are never link codes, so they stay readable in the
# log. Story 3.1 adds `admin`. Anything not listed here is masked: masking too
# much only makes a log line less helpful, masking too little leaks a login.
NOT_LINK_CODES = frozenset({"static", "stil", "robots.txt"})

# A request path starts with `/` at the start of the message or after
# whitespace, a quote or `(`; its first segment runs to the next `/`, space,
# query, fragment or quote. `HTTP/1.1` and `http://` are not paths: their `/`
# follows a letter or another `/`.
_REQUEST_PATH = re.compile(r"""(?<![^\s"'(])/(?P<segment>[^/\s?#"']+)""")


def _mask(match: re.Match[str]) -> str:
    if match["segment"] in NOT_LINK_CODES:
        return match[0]
    return "/[code]"


def mask_link_codes(message: str) -> str:
    """NFR-4, AD-15: `message` with the first segment of every request path as `[code]`.

    Any first segment is masked, not only 22-character ones, because a mistyped
    code is nearly a real one. `/`, `HTTP/1.1` and paths under `NOT_LINK_CODES`
    are left as they are.
    """
    return _REQUEST_PATH.sub(_mask, message)


class MaskLinkCodes(logging.Filter):
    """NFR-4, AD-15: masks link codes in every record a handler writes.

    The message is formatted first (`getMessage()`), because Django passes the
    path as an argument, then masked and stored back with no arguments left.
    It never drops a record.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = mask_link_codes(record.getMessage())
        record.args = ()
        return True
