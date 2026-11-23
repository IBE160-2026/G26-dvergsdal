"""Joining words in Norwegian text (Story 2.5; FR-21, FR-28).

A leaf module with no imports from the form, so both forms.py and summary.py
can use it.
"""

from collections.abc import Sequence


def join_words(words: Sequence[str]) -> str:
    """FR-21, FR-28: words joined «a», «a og b» or «a, b og c»."""
    if len(words) <= 1:
        return "".join(words)
    return f"{', '.join(words[:-1])} og {words[-1]}"
