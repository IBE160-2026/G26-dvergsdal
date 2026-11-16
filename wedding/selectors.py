"""Read queries for views and commands (Structural Seed).

Selectors load facts from the models and never filter on answer content; counts
and totals come from `wedding.rules` (AD-2).
"""

from collections.abc import Iterable

from wedding.models import Guest, User


def test_data_conflicts(codes: Iterable[str], usernames: Iterable[str]) -> list[str]:
    """FR-72, AD-16: the seed codes and usernames already used by rows that are not test data.

    The seed command stops before writing anything when this is not empty, so it
    never replaces a real guest's link or a real account. Each item names the
    code or username in Norwegian; codes come first, in the order given.
    """
    codes = list(codes)
    usernames = list(usernames)
    taken_codes = set(
        Guest.objects.filter(code__in=codes, household__is_test_data=False).values_list(
            "code", flat=True
        )
    )
    taken_usernames = set(
        User.objects.filter(username__in=usernames, is_test_data=False).values_list(
            "username", flat=True
        )
    )
    return [f"lenkekoden «{code}»" for code in codes if code in taken_codes] + [
        f"brukernavnet «{username}»" for username in usernames if username in taken_usernames
    ]
