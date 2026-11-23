"""The answer deadline: when guests can no longer answer (Story 2.1).

FR-41, AD-11: the deadline is a date, and guests can answer until 23:59:59
Oslo time that day. From 00:00:00 Europe/Oslo on the day after, it has passed.
`zoneinfo` gives the Oslo offset on each date, so a summer or winter deadline,
and the two days the clocks change, all close at Oslo midnight. `now` is passed
in, so the rule never reads a clock (AD-2).
"""

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

OSLO = ZoneInfo("Europe/Oslo")


def is_past_deadline(deadline: date, now: datetime) -> bool:
    """FR-41, AD-11: True from 00:00:00 Oslo time on the day after `deadline`.

    `now` must be aware (Django's `timezone.now()` is UTC); a naive `now` has no
    known moment, so it raises `ValueError` instead of guessing a zone.
    """
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be an aware datetime")
    closes = datetime.combine(deadline + timedelta(days=1), time(0), tzinfo=OSLO)
    return now >= closes
