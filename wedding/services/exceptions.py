"""The errors services raise when they refuse a write (AD-3, AD-10, NFR-6).

Views catch them and show `message` to the user, so every message is in
Norwegian bokmål. A refused write has written nothing.
"""


class ServiceError(Exception):
    """A service refused to write; `message` is shown to the user as it is."""

    default_message = "Endringen ble ikke lagret."

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class NotAllowed(ServiceError):
    """AD-10: the actor may not make this change, for example a helper."""

    default_message = "Du har ikke lov til å gjøre denne endringen."


class InvalidHousehold(ServiceError):
    """FR-49, AD-8: the household or one of its guests is not valid."""

    default_message = "Husstanden ble ikke lagret."


class InvalidUser(ServiceError):
    """FR-47, AD-10: the admin account is not valid, for example a taken username."""

    default_message = "Brukeren ble ikke lagret."


class InvalidSettings(ServiceError):
    """FR-64, AD-12: a setting is not valid, for example a negative price."""

    default_message = "Innstillingene ble ikke lagret."


class DeadlinePassed(ServiceError):
    """FR-41, AD-11 (Story 2.6a): a guest sent an answer after the deadline."""

    default_message = "Svarfristen har gått ut."


class InvalidAnswer(ServiceError):
    """FR-74, AD-9 (Story 2.6a): the answer does not cover the household as it is now."""

    default_message = "Svaret ble ikke sendt."


class RevisionConflict(ServiceError):
    """AD-9, FR-74 (Story 2.6c): the household's answer was sent after the draft started.

    `revision` is the household's current revision, so the view can move the
    draft onto it; the next send is then a new send.
    """

    default_message = "Svaret ble ikke sendt, fordi svaret for husstanden er endret."

    def __init__(self, message: str | None = None, *, revision: int):
        self.revision = revision
        super().__init__(message)


class TotalChanged(ServiceError):
    """AD-7, NFR-2 (Story 2.6c): the total differs from the one the check page showed."""

    default_message = "Svaret ble ikke sendt, fordi summen har endret seg."


class ConsentTextChanged(ServiceError):
    """AD-18, FR-29 (Story 2.6c): the consent text changed after the guest answered it."""

    default_message = "Svaret ble ikke sendt, fordi teksten om samtykke er endret."
