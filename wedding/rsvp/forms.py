"""The RSVP form's Django forms and their texts (Stories 2.1 to 2.3).

FR-13, FR-14, FR-22: step 1 asks, for each household member, «Kommer» or
«Kommer ikke», with nothing chosen in advance. Step 2 asks whether everyone
coming is there the whole weekend, «Ja» or «Nei», and after «Nei» which days
each coming person comes (FR-14, FR-70). Step 3 asks each coming person
«Ja» or «Nei» to a cabin for the whole weekend, and step 4 which paid meals
each wants, both with their prices and why guests pay (FR-15, FR-16, FR-32,
FR-70, FR-73, Story 2.3). The server validates every POST; a
missing or forged value is an error on that group. The templates write the
inputs themselves, so the markup follows DESIGN.md's choice control and error
line exactly; the forms validate, say what was posted, and hold each step's
choice labels, error lines and error-summary texts. The texts of steps 2 to
4 are avgjort av Claude 2026-11-23 (EXPERIENCE.md, Microcopy).
"""

from django import forms

from wedding.rsvp.steps import DAYS, MEALS
from wedding.rules.days import DAY_KEYS, GAP, NO_DAY
from wedding.templatetags.money import kroner

YES = "yes"
NO = "no"
ATTENDANCE_CHOICES = ((YES, "Kommer"), (NO, "Kommer ikke"))
WHOLE_CHOICES = (
    (YES, "Ja, alle er med fra fredag til søndag"),
    (NO, "Nei, jeg velger dager for hver person"),
)
WHOLE_FIELD = "whole"
# FR-32: the en dash between a choice and its price, as on the mockup.
DASH = "\N{EN DASH}"

# FR-32: why guests pay, on steps 3 and 4 (avgjort av Claude 2026-11-23).
PAY_NOTE = (
    "Dette er Hardingasetes priser, og hver gjest betaler selv. "
    "Lunsj og middag på bryllupsdagen dekker vi."
)


def attendance_field(guest_id: int) -> str:
    """FR-13: the POST name of a member's attendance radios."""
    return f"attendance_{guest_id}"


def days_field(guest_id: int) -> str:
    """FR-14: the POST name of a member's day checkboxes."""
    return f"days_{guest_id}"


def overnight_field(guest_id: int) -> str:
    """FR-16: the POST name of a member's overnight radios."""
    return f"overnight_{guest_id}"


def meals_field(guest_id: int) -> str:
    """FR-15: the POST name of a member's meal checkboxes."""
    return f"meals_{guest_id}"


def _priced(label: str, price: int) -> str:
    """FR-32: the label, a dash and the price, or the label alone at price 0 (Rikke 2026-11-21)."""
    return f"{label} {DASH} {kroner(price)}" if price else label


class WhoIsComingForm(forms.Form):
    """FR-12, FR-13, FR-14, FR-22: step 1, «Hvem kommer?», one required choice per member.

    `members` is the household as (id, name), from `household_members`. A value
    other than «yes» or «no», or a field for someone outside the household, is
    never accepted.
    """

    def __init__(self, members: list[tuple[int, str]], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.members = members
        for guest_id, name in members:
            message = self.error_text(name)
            self.fields[attendance_field(guest_id)] = forms.ChoiceField(
                label=name,
                choices=ATTENDANCE_CHOICES,
                widget=forms.RadioSelect,
                error_messages={"required": message, "invalid_choice": message},
            )

    @staticmethod
    def error_text(name: str) -> str:
        """FR-22: the error line under a member's legend when they have no answer."""
        return f"Velg «Kommer» eller «Kommer ikke» for {name}."

    @staticmethod
    def summary_text(name: str) -> str:
        """FR-22, UX-DR16: the error summary's link to that member's group."""
        return f"Velg om {name} kommer"

    def attendance(self) -> dict[int, bool]:
        """FR-13: each member's validated attendance; only after `is_valid()`."""
        return {
            guest_id: self.cleaned_data[attendance_field(guest_id)] == YES
            for guest_id, _ in self.members
        }

    def posted_attendance(self) -> dict[int, bool]:
        """FR-13: the members whose posted value is valid, without requiring the others.

        Used by «Velg» and by an invalid «Fortsett» (the answers chosen so far
        are kept in the draft) and by the re-render after a CSRF failure
        (UX-DR52).
        """
        posted = {}
        for guest_id, _ in self.members:
            value = self.data.get(attendance_field(guest_id))
            if value in (YES, NO):
                posted[guest_id] = value == YES
        return posted


class DaysForm(forms.Form):
    """FR-14, FR-22, FR-70: step 2, «Er alle som kommer, med hele helgen?».

    `whole` is «yes» or «no»; after «Nei», `days_<id>` holds the ticked day
    keys of each coming member. `coming` is the coming members as (id, name).
    Whether a set of days is allowed is the rule `day_error`
    (wedding/rules/days.py); this form only reads what was posted, ignoring a
    forged value, a day key that does not exist and a member who is not coming.
    """

    WHOLE_ERROR = "Velg «Ja» eller «Nei»."
    WHOLE_SUMMARY = "Svar på om alle er med hele helgen"

    def __init__(self, coming: list[tuple[int, str]], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.coming = coming

    @staticmethod
    def day_error_text(name: str, problem: str) -> str:
        """FR-14, FR-22, FR-70: the error line for a member's `day_error` result."""
        if problem == NO_DAY:
            return f"Velg minst én dag for {name}."
        if problem == GAP:
            return (
                f"{name} kan ikke komme fredag og søndag uten lørdag, fordi dagene må komme "
                "etter hverandre. Velg lørdag også, eller bare én av dagene."
            )
        raise ValueError(f"Unknown day problem: {problem}")

    @staticmethod
    def day_summary_text(name: str) -> str:
        """FR-22, UX-DR16: the error summary's link to a member's day group."""
        return f"Velg dager for {name}"

    def posted_whole(self) -> bool | None:
        """FR-14: True for «Ja», False for «Nei», None when missing or forged."""
        value = self.data.get(WHOLE_FIELD)
        if value in (YES, NO):
            return value == YES
        return None

    def has_posted_days(self) -> bool:
        """FR-14: whether any day checkbox of a coming member was posted."""
        return any(days_field(guest_id) in self.data for guest_id, _ in self.coming)

    def posted_days(self) -> dict[int, list[str]]:
        """FR-14: each coming member's valid ticked day keys, in `DAY_KEYS` order."""
        days = {}
        for guest_id, _ in self.coming:
            ticked = set(self.data.getlist(days_field(guest_id)))
            days[guest_id] = [day for day in DAY_KEYS if day in ticked]
        return days


class OvernightForm(forms.Form):
    """FR-16, FR-22, FR-32, FR-70: step 3, «Hvem skal overnatte på Hardingasete?».

    `overnight_<id>` is «yes» or «no» for each coming member; `coming` is
    them as (id, name). Whether a person can stay is the rule
    `can_stay_overnight` (wedding/rules/days.py); this form reads what was
    posted, ignoring a forged value and a member who is not coming, and holds
    the step's texts.
    """

    PRICE_LABEL = "Hytte hele helgen"
    PRICE_UNIT = "per person"
    YES_LABEL = "Ja, hytte hele helgen"
    NO_LABEL = "Nei"

    def __init__(self, coming: list[tuple[int, str]], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.coming = coming

    @staticmethod
    def lead() -> str:
        """FR-16, FR-70: why the cabin is paid for both nights, with the dates from `DAYS`."""
        first, last = DAYS[DAY_KEYS[0]], DAYS[DAY_KEYS[-1]]
        return (
            f"Hyttene er leid for hele helgen, fra {first.name.lower()} {first.date} til "
            f"{last.name.lower()} {last.date}. Begge nettene betales, også for den som bare "
            "sover der én natt."
        )

    @classmethod
    def choices(cls, price: int) -> tuple[tuple[str, str], ...]:
        """FR-16, FR-32: «Ja, hytte hele helgen» with the price, and «Nei»."""
        return ((YES, _priced(cls.YES_LABEL, price)), (NO, cls.NO_LABEL))

    @staticmethod
    def error_text(name: str) -> str:
        """FR-22: the error line under a member's legend when they have no answer."""
        return f"Velg «Ja» eller «Nei» for {name}."

    @staticmethod
    def blocked_text(name: str, days: list[str]) -> str:
        """FR-22, FR-70: the error line for a member whose days do not allow a stay."""
        day_names = " og ".join(DAYS[day].name.lower() for day in DAY_KEYS if day in days)
        return (
            "For å overnatte må man være med minst to dager på rad, og "
            f"{name} kommer bare {day_names}. Velg «Nei», eller gå tilbake og velg flere "
            f"dager for {name}."
        )

    @staticmethod
    def summary_text(name: str) -> str:
        """FR-22, UX-DR16: the error summary's link to a member's overnight group."""
        return f"Velg overnatting for {name}"

    def posted_night(self) -> dict[int, bool]:
        """FR-16: each coming member's valid posted «Ja» (True) or «Nei» (False)."""
        posted = {}
        for guest_id, _ in self.coming:
            value = self.data.get(overnight_field(guest_id))
            if value in (YES, NO):
                posted[guest_id] = value == YES
        return posted


class MealsForm(forms.Form):
    """FR-15, FR-32, FR-73: step 4, «Hvilke måltider skal vi bestille?».

    `meals_<id>` holds the ticked meal keys of each member in `shown`, given
    as (id, name, offered meal keys) for every coming member who is offered a
    paid meal (`offered_meals`, wedding/rules/days.py). Choosing no meal is
    fine, so there is nothing to refuse: a forged key or a meal not offered to
    that member is ignored.
    """

    HINT = "Kryss av for måltidene hver person skal ha. Det er greit å ikke velge noen."

    def __init__(self, shown: list[tuple[int, str, tuple[str, ...]]], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.shown = shown

    @staticmethod
    def meal_label(key: str, price: int) -> str:
        """FR-15, FR-32: the meal's name with its price, as «Middag fredag» and 340 kr."""
        return _priced(MEALS[key].name, price)

    def posted_meals(self) -> dict[int, list[str]]:
        """FR-15, FR-73: each shown member's ticked offered meal keys, in offered order."""
        meals = {}
        for guest_id, _, offered in self.shown:
            ticked = set(self.data.getlist(meals_field(guest_id)))
            meals[guest_id] = [meal for meal in offered if meal in ticked]
        return meals


def posted_respondent(data, member_ids: set[int]) -> int | None:
    """FR-12: the posted respondent's guest id when it is a household member, else None."""
    value = data.get("respondent", "")
    if value.isascii() and value.isdigit() and int(value) in member_ids:
        return int(value)
    return None
