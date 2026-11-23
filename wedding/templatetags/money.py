"""`kroner`: one way to show an amount, on the programme and in the RSVP form (Story 2.3).

FR-32, FR-33, AD-12: every amount is a whole number of kroner. The filter
writes it with a no-break space between the thousands and before «kr», so
«1 500 kr» never breaks over two lines: 0 → «0 kr», 340 → «340 kr»,
1450 → «1 450 kr». Load it with `{% load money %}`.
"""

from django import template

register = template.Library()

NO_BREAK_SPACE = "\N{NO-BREAK SPACE}"


@register.filter(is_safe=True)
def kroner(amount: int) -> str:
    """FR-32, FR-33: `amount` whole kroner as «1 450 kr», with no-break spaces."""
    return f"{amount:,}".replace(",", NO_BREAK_SPACE) + f"{NO_BREAK_SPACE}kr"
