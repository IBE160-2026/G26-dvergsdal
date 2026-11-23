"""The answer deadline rule, `is_past_deadline` (Story 2.1).

FR-41, AD-11: guests can answer until 23:59:59.999999 Oslo time on the
deadline date, and the deadline has passed from 00:00:00 Oslo time the day
after. Table-driven over both sides of the boundary, a winter and a summer
deadline (23:00Z and 22:00Z), both days the clocks change in 2028 (26 March
and 29 October) and the days before them, and a naive `now`.
"""

from datetime import UTC, date, datetime, timedelta

import pytest

from wedding.rules.deadline import OSLO, is_past_deadline

# (deadline, the first moment it has passed, in UTC)
CLOSES_AT = [
    (date(2028, 1, 4), datetime(2028, 1, 4, 23, 0, tzinfo=UTC)),  # winter, CET
    (date(2028, 5, 27), datetime(2028, 5, 27, 22, 0, tzinfo=UTC)),  # summer, CEST
    (date(2028, 3, 25), datetime(2028, 3, 25, 23, 0, tzinfo=UTC)),  # midnight before the change
    (date(2028, 3, 26), datetime(2028, 3, 26, 22, 0, tzinfo=UTC)),  # clocks went forward
    (date(2028, 10, 28), datetime(2028, 10, 28, 22, 0, tzinfo=UTC)),  # midnight before the change
    (date(2028, 10, 29), datetime(2028, 10, 29, 23, 0, tzinfo=UTC)),  # clocks went back
]


@pytest.mark.parametrize(("deadline", "closes"), CLOSES_AT)
def test_the_deadline_passes_at_oslo_midnight(deadline, closes):
    """FR-41, AD-11: open one microsecond before Oslo midnight, passed at it."""
    assert not is_past_deadline(deadline, closes - timedelta(microseconds=1))
    assert is_past_deadline(deadline, closes)
    assert is_past_deadline(deadline, closes + timedelta(days=30))


@pytest.mark.parametrize(("deadline", "closes"), CLOSES_AT)
def test_the_boundary_in_oslo_time(deadline, closes):
    """FR-41: 23:59:59.999999 on the deadline in Oslo is open; 00:00:00 the next day is not."""
    last = datetime.combine(deadline, datetime.max.time(), tzinfo=OSLO)
    first = datetime.combine(deadline + timedelta(days=1), datetime.min.time(), tzinfo=OSLO)
    assert not is_past_deadline(deadline, last)
    assert is_past_deadline(deadline, first)
    assert first == closes


@pytest.mark.parametrize(
    "now",
    [
        datetime(2028, 1, 1, 12, 0, tzinfo=UTC),
        datetime(2028, 1, 4, 0, 0, tzinfo=OSLO),
        datetime(2027, 12, 31, 23, 59, tzinfo=OSLO),
    ],
)
def test_before_and_on_the_deadline_day_it_is_open(now):
    """FR-41: the whole deadline day and every day before it are open."""
    assert not is_past_deadline(date(2028, 1, 4), now)


def test_a_naive_now_is_refused():
    """AD-11: a naive `now` has no known moment, so the rule refuses to guess."""
    with pytest.raises(ValueError, match="aware"):
        is_past_deadline(date(2028, 1, 4), datetime(2028, 1, 5, 12, 0))
