"""How many people a household may have (FR-49, AD-8).

A household has at least one person and at most 8. The upper limit keeps a full
RSVP draft inside the 4 KB cookie (AD-8); Rikke confirmed that no household on
the guest list is larger.
"""

MIN_HOUSEHOLD_SIZE = 1
MAX_HOUSEHOLD_SIZE = 8


def household_size_problem(count: int) -> str | None:
    """FR-49, AD-8: a Norwegian message when `count` people is not a valid household, else None."""
    if count < MIN_HOUSEHOLD_SIZE:
        return "En husstand må ha minst én person."
    if count > MAX_HOUSEHOLD_SIZE:
        return f"En husstand kan ha høyst {MAX_HOUSEHOLD_SIZE} personer."
    return None
