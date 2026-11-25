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

FR-34, FR-36, AD-12 (Story 2.7): what a household still owes is the total
less the amount it has reported paid (`guest_balance`); until Story 5.1 adds
«Jeg har betalt» there is no report, so it is the total.
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


def guest_balance(total: int, report: int | None) -> int:
    """FR-34, FR-36, AD-12: what the guest is shown as left to pay, never below 0.

    `total` is `household_total`; `report` is the amount the household has
    reported paid, None while it has reported nothing (always None until
    Story 5.1). The receipt offers «Betal nå» only when this is above 0.
    """
    return max(total - (report or 0), 0)
