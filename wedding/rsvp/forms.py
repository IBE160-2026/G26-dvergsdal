"""The RSVP form's Django forms (Story 2.1).

FR-13, FR-14, FR-22: step 1 asks, for each household member, «Kommer» or
«Kommer ikke», with nothing chosen in advance. The server validates every
POST; a missing or forged value is an error on that person's group. The
templates write the radios themselves, so the markup follows DESIGN.md's
choice control and error line exactly; the form only validates and says what
was posted.
"""

from django import forms

COMING = "yes"
NOT_COMING = "no"
ATTENDANCE_CHOICES = ((COMING, "Kommer"), (NOT_COMING, "Kommer ikke"))


def attendance_field(guest_id: int) -> str:
    """FR-13: the POST name of a member's attendance radios."""
    return f"attendance_{guest_id}"


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
            message = f"Velg «Kommer» eller «Kommer ikke» for {name}."
            self.fields[attendance_field(guest_id)] = forms.ChoiceField(
                label=name,
                choices=ATTENDANCE_CHOICES,
                widget=forms.RadioSelect,
                error_messages={"required": message, "invalid_choice": message},
            )

    def attendance(self) -> dict[int, bool]:
        """FR-13: each member's validated attendance; only after `is_valid()`."""
        return {
            guest_id: self.cleaned_data[attendance_field(guest_id)] == COMING
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
            if value in (COMING, NOT_COMING):
                posted[guest_id] = value == COMING
        return posted


def posted_respondent(data, member_ids: set[int]) -> int | None:
    """FR-12: the posted respondent's guest id when it is a household member, else None."""
    value = data.get("respondent", "")
    if value.isascii() and value.isdigit() and int(value) in member_ids:
        return int(value)
    return None
