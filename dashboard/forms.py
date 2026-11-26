"""The login form (FR-46, NFR-4, AD-10).

Every way a login can fail, whether the password is wrong, the username is
unknown, the account is inactive or the role is not valid, gives the same
sentence, so the page never says which usernames exist.
"""

from typing import ClassVar

from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from wedding.models import User

LOGIN_FAILED = "Brukernavnet eller passordet stemmer ikke. Prøv igjen."


class AdminLoginForm(AuthenticationForm):
    """FR-46, NFR-4: Django's login form with Norwegian messages and a role check."""

    error_messages: ClassVar[dict[str, str]] = {
        "invalid_login": LOGIN_FAILED,
        "inactive": LOGIN_FAILED,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].error_messages["required"] = "Skriv inn brukernavnet."
        self.fields["password"].error_messages["required"] = "Skriv inn passordet."

    def confirm_login_allowed(self, user: User) -> None:
        """AD-10: refuse an inactive account or one without a valid role, with the same text."""
        super().confirm_login_allowed(user)
        if user.role not in User.Role.values:
            raise ValidationError(self.error_messages["invalid_login"], code="invalid_login")
