"""The couple's phone numbers as `tel:` links (FR-6, Story 1.5).

The footer band on every valid-link page shows each number as the couple typed
it and links it with `tel:`, which takes only a leading `+` and digits.
"""

import re

_DIGIT = re.compile(r"[0-9]")
# «+47 (0) 900 00 000»: the trunk 0 in brackets is not dialled after a country code.
_TRUNK_PREFIX = re.compile(r"\(\s*0\s*\)")


def tel_number(phone: str) -> str:
    """FR-6: `phone` for a `tel:` link: a leading `+` and the digits only.

    «+47 000 00 101» gives «+4700000101», «(+47) 900-00-000» and
    «+47 (0) 900 00 000» both «+4790000000». A `+` counts only before the first
    digit, and a «(0)» trunk prefix is dropped. Without a digit the result is
    `""`, and the footer leaves that contact out.
    """
    phone = _TRUNK_PREFIX.sub("", phone)
    first_digit = _DIGIT.search(phone)
    if first_digit is None:
        return ""
    plus = "+" if "+" in phone[: first_digit.start()] else ""
    return plus + "".join(_DIGIT.findall(phone))
