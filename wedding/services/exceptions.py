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
