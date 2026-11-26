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


def digits_only(text: str) -> str:
    """FR-34, FR-64: `text` with everything but its digits removed.

    «1234.56.78900» copies as «12345678900», since bank and Vipps fields
    reject dots and spaces.
    """
    return "".join(char for char in text if char.isdigit())


def guest_balance(total: int, report: int | None) -> int:
    """FR-34, FR-36, AD-12: what the guest is shown as left to pay, never below 0.

    `total` is `household_total`; `report` is the amount the household has
    reported paid, None while it has reported nothing (always None until
    Story 5.1). The receipt offers «Betal nå» only when this is above 0.
    """
    return max(total - (report or 0), 0)


# FR-60: a household's payment statuses (Story 3.2; `refund_owed` and the
# amounts behind them come with Stories 5.2 and 5.3).
PAID = "paid"
PART_PAID = "part_paid"
NOT_PAID = "not_paid"
NOTHING_TO_PAY = "nothing_to_pay"
REFUND_OWED = "refund_owed"
PAYMENT_NOT_ANSWERED = "not_answered"


def payment_status(answered: bool, total: int, received: int, refunded: int) -> str:
    """FR-60, FR-74, AD-2, AD-12: a household's payment status.

    Not answered gives `not_answered` whatever the amounts. Otherwise the net
    is `received` less `refunded`: nothing to pay when `total` and the net are
    both 0, `refund_owed` when the net is above `total`, `paid` when equal,
    `part_paid` when above 0 but below `total`, else `not_paid`.
    """
    if not answered:
        return PAYMENT_NOT_ANSWERED
    net = received - refunded
    if total == 0 and net == 0:
        return NOTHING_TO_PAY
    if net > total:
        return REFUND_OWED
    if net == total:
        return PAID
    return PART_PAID if net > 0 else NOT_PAID
