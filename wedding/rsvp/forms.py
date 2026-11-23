"""The RSVP form's Django forms and their texts (Stories 2.1, 2.2).

FR-13, FR-14, FR-22: step 1 asks, for each household member, «Kommer» or
«Kommer ikke», with nothing chosen in advance. Step 2 asks whether everyone
coming is there the whole weekend, «Ja» or «Nei», and after «Nei» which days
each coming person comes (FR-14, FR-70). The server validates every POST; a
missing or forged value is an error on that group. The templates write the
inputs themselves, so the markup follows DESIGN.md's choice control and error
line exactly; the forms validate, say what was posted, and hold each step's
choice labels, error lines and error-summary texts. The texts marked
[forslag] in EXPERIENCE.md are proposals.
"""

from django import forms

from wedding.rules.days import DAY_KEYS, GAP, NO_DAY

YES = "yes"
NO = "no"
ATTENDANCE_CHOICES = ((YES, "Kommer"), (NO, "Kommer ikke"))
WHOLE_CHOICES = (
    (YES, "Ja, alle er med fra fredag til søndag"),
    (NO, "Nei, jeg velger dager for hver person"),
)
WHOLE_FIELD = "whole"


def attendance_field(guest_id: int) -> str:
    """FR-13: the POST name of a member's attendance radios."""
    return f"attendance_{guest_id}"


def days_field(guest_id: int) -> str:
    """FR-14: the POST name of a member's day checkboxes."""
    return f"days_{guest_id}"


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


def posted_respondent(data, member_ids: set[int]) -> int | None:
    """FR-12: the posted respondent's guest id when it is a household member, else None."""
    value = data.get("respondent", "")
    if value.isascii() and value.isdigit() and int(value) in member_ids:
        return int(value)
    return None
