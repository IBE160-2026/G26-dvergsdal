"""The RSVP form's Django forms and their texts (Stories 2.1 to 2.5).

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

Step 5 (Story 2.4; FR-25 to FR-28, UX-DR21) asks each coming person for
«Ingen allergier eller matbehov» or fixed categories and a short note, and a
«Ja»/«Nei» to storing it, starting unanswered; for anyone but the respondent,
«Jeg bekrefter at <name> vet om dette og er enig». Its texts are avgjort av
Claude 2026-11-23 (EXPERIENCE.md, Microcopy).

Step 6 (Story 2.5; FR-17, FR-22) asks each coming person present on Friday
«Ja», «Nei» or «Kanskje» to the Friday hike, with nothing chosen in advance;
its texts are avgjort av Claude 2026-11-23 (EXPERIENCE.md, Microcopy).
"""

from django import forms

from wedding.rsvp.steps import ALLERGIES, DAYS, HIKE, MEALS
from wedding.rsvp.summary import join_words
from wedding.rules.allergies import NOTE_MAX, AllergyEntry, clean_note
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


def allergy_field(guest_id: int) -> str:
    """FR-25: the POST name of a member's allergy category checkboxes."""
    return f"allergies_{guest_id}"


def allergy_none_field(guest_id: int) -> str:
    """FR-25: the POST name of a member's «Ingen allergier eller matbehov» checkbox."""
    return f"allergy_none_{guest_id}"


def note_field(guest_id: int) -> str:
    """FR-25: the POST name of a member's allergy note."""
    return f"note_{guest_id}"


def consent_field(guest_id: int) -> str:
    """FR-26: the POST name of a member's consent radios."""
    return f"consent_{guest_id}"


def confirm_field(guest_id: int) -> str:
    """FR-27: the POST name of the respondent's confirmation for a member."""
    return f"confirm_{guest_id}"


def hike_field(guest_id: int) -> str:
    """FR-17: the POST name of a member's hike radios."""
    return f"hike_{guest_id}"


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


class AllergiesForm(forms.Form):
    """FR-25 to FR-28, UX-DR21: step 5, «Allergier og matbehov».

    For each coming member in `coming` (id, name): `allergy_none_<id>`
    («yes»), `allergies_<id>` (category keys), `note_<id>`, `consent_<id>`
    («yes»/«no») and `confirm_<id>` («yes»). Whether an answer is complete is
    the rule `allergy_problems` (wedding/rules/allergies.py); this form reads
    what was posted, ignoring forged values and members who are not coming,
    and holds the step's texts.
    """

    LEAD = "Dette er valgfritt."
    NONE_LABEL = "Ingen allergier eller matbehov"
    OR_LINE = "Eller kryss av for det som gjelder:"
    NOTE_HINT = f"Skriv bare det kjøkkenet trenger å vite, ingen diagnoser. Høyst {NOTE_MAX} tegn."
    CONSENT_CHOICES = ((YES, "Ja"), (NO, "Nei"))

    def __init__(self, coming: list[tuple[int, str]], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.coming = coming

    @staticmethod
    def categories() -> list[tuple[str, str]]:
        """FR-25: the fixed categories as (key, label), in form order."""
        return list(ALLERGIES.items())

    @staticmethod
    def note_label(name: str) -> str:
        """FR-25: the note's label."""
        return f"Kort merknad om {name} (valgfritt)"

    @staticmethod
    def consent_legend(name: str) -> str:
        """FR-26: the legend of a member's consent group."""
        return f"Får vi lagre opplysningene om {name}?"

    @staticmethod
    def confirm_label(name: str) -> str:
        """FR-27: the confirmation when answering for someone else."""
        return f"Jeg bekrefter at {name} vet om dette og er enig"

    @staticmethod
    def conflict_text(name: str) -> str:
        """FR-22, UX-DR21: the error line when «Ingen …» is ticked with something else."""
        return (
            "Du har krysset av for «Ingen allergier eller matbehov» og fylt inn noe annet "
            f"for {name}. Velg det ene."
        )

    @staticmethod
    def conflict_summary(name: str) -> str:
        """FR-22, UX-DR16: the summary link for a conflict."""
        return f"Rett opp allergiene for {name}"

    @staticmethod
    def confirm_text(name: str) -> str:
        """FR-22, FR-27: the error line under a missing confirmation."""
        return f"Kryss av for at {name} vet om dette og er enig, eller svar «Nei» på samtykket."

    @staticmethod
    def confirm_summary(name: str) -> str:
        """FR-22, UX-DR16: the summary link for a missing confirmation."""
        return f"Bekreft for {name}"

    @staticmethod
    def long_text(name: str) -> str:
        """FR-22, FR-25: the error line for a note over `NOTE_MAX` characters."""
        return f"Merknaden om {name} kan være høyst {NOTE_MAX} tegn."

    @staticmethod
    def long_summary(name: str) -> str:
        """FR-22, UX-DR16: the summary link for a note that is too long."""
        return f"Kort ned merknaden om {name}"

    @staticmethod
    def warning_text(names: list[str]) -> str:
        """FR-28: the warning when someone's allergy information will not be saved."""
        return (
            f"Allergiopplysningene om {join_words(names)} blir ikke lagret uten et «Ja» til "
            "samtykke. "
            "Dere kan sende svaret likevel, og heller si fra til oss direkte."
        )

    def _note(self, guest_id: int) -> str:
        return clean_note(self.data.get(note_field(guest_id), ""))

    def long_notes(self) -> list[int]:
        """FR-25: the coming members whose posted note is longer than `NOTE_MAX`."""
        return [guest_id for guest_id, _ in self.coming if len(self._note(guest_id)) > NOTE_MAX]

    def posted_entries(self, previous: dict[int, AllergyEntry] | None) -> dict[int, AllergyEntry]:
        """FR-25: each coming member's posted entry.

        Unknown category keys are ignored. A note over `NOTE_MAX` characters
        is replaced by the member's note in `previous`, so it never reaches
        the draft; with `previous` None (the CSRF re-render) it is kept as
        posted.
        """
        entries = {}
        for guest_id, _ in self.coming:
            ticked = set(self.data.getlist(allergy_field(guest_id)))
            note = self._note(guest_id)
            if previous is not None and len(note) > NOTE_MAX:
                note = previous.get(guest_id, AllergyEntry()).note
            entries[guest_id] = AllergyEntry(
                cats=tuple(key for key in ALLERGIES if key in ticked),
                none=self.data.get(allergy_none_field(guest_id)) == YES,
                note=note,
            )
        return entries

    def posted_consent(self) -> dict[int, bool]:
        """FR-26: each coming member's posted «Ja» (True) or «Nei» (False)."""
        posted = {}
        for guest_id, _ in self.coming:
            value = self.data.get(consent_field(guest_id))
            if value in (YES, NO):
                posted[guest_id] = value == YES
        return posted

    def posted_confirmed(self, respondent: int) -> list[int]:
        """FR-27: the coming members other than `respondent` whose confirmation was ticked."""
        return [
            guest_id
            for guest_id, _ in self.coming
            if guest_id != respondent and self.data.get(confirm_field(guest_id)) == YES
        ]


class HikeForm(forms.Form):
    """FR-17, FR-22: step 6, «Hvem blir med på fjellturen fredag?».

    `hike_<id>` is «yes», «no» or «maybe» for each member in `asked`, given
    as (id, name) for every coming member present on Friday. This form reads
    what was posted, ignoring a forged value and anyone not asked, and holds
    the step's texts.
    """

    LEAD = (
        "Fjellturen er fredag, for dem som kommer tidlig. "
        "Svar «Kanskje» hvis dere ikke har bestemt dere ennå."
    )
    CHOICES = tuple(HIKE.items())

    def __init__(self, asked: list[tuple[int, str]], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.asked = asked

    @staticmethod
    def error_text(name: str) -> str:
        """FR-22: the error line under a member's legend when they have no answer."""
        return f"Velg «Ja», «Nei» eller «Kanskje» for {name}."

    @staticmethod
    def summary_text(name: str) -> str:
        """FR-22, UX-DR16: the error summary's link to a member's hike group."""
        return f"Svar om fjellturen for {name}"

    def posted_hike(self) -> dict[int, str]:
        """FR-17: each asked member's valid posted answer key."""
        posted = {}
        for guest_id, _ in self.asked:
            value = self.data.get(hike_field(guest_id))
            if value in HIKE:
                posted[guest_id] = value
        return posted


def posted_respondent(data, member_ids: set[int]) -> int | None:
    """FR-12: the posted respondent's guest id when it is a household member, else None."""
    value = data.get("respondent", "")
    if value.isascii() and value.isdigit() and int(value) in member_ids:
        return int(value)
    return None
