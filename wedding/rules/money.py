"""What a household pays the venue (Story 2.3).

FR-33, AD-12, NFR-2: the household total is always computed from the answer
and the current prices, in whole kroner, and never stored. `household_total`
is the only place it is computed: the form's running total, the check page,
the receipt and the couple's numbers all call it, and no view or template
adds prices itself.

FR-16, FR-32: a cabin is booked and paid for the whole weekend, per person
who stays (expected.toml), and each chosen paid meal costs its price.
`prices` holds the price of the cabin under `CABIN` and each meal under its
key in `MEAL_KEYS` (wedding/selectors.py, `form_prices`).
"""

from collections.abc import Mapping

from wedding.rules.answer import Answer, normalise_answer

CABIN = "cabin_weekend"


def household_total(answer: Answer, prices: Mapping[str, int]) -> int:
    """FR-33, AD-12, NFR-2: the household's total in whole kroner.

    The answer is normalised first (FR-75), so a stay or a meal for someone
    who is not coming, or whose days no longer allow it, never counts. Then
    the cabin price for each «Ja» to overnight stay and each chosen meal's
    price.
    """
    answer = normalise_answer(answer)
    cabins = sum(prices[CABIN] for stays in answer.night.values() if stays)
    meals = sum(prices[meal] for chosen in answer.meals.values() for meal in chosen)
    return int(cabins + meals)
