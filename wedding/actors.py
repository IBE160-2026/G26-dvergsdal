"""Who is acting: a guest, an admin user or the system (AD-3, AD-6, AD-10).

Every service takes one of these as an explicit `actor`, never the request, and
records it as the author of the write. A guest actor comes only from the resolver
in `wedding/links.py`; the system actor is used only by the seed command. This
module only describes actors and writes nothing.
"""

from dataclasses import dataclass

from wedding.models import Guest, Household, User


@dataclass(frozen=True)
class GuestActor:
    """A guest who opened their personal link, and their household (AD-6, FR-2)."""

    guest: Guest
    household: Household


@dataclass(frozen=True)
class AdminActor:
    """A logged-in couple or helper account (AD-10, FR-46)."""

    user: User

    @property
    def is_couple(self) -> bool:
        """AD-10: only the couple may write; helpers read."""
        return self.user.role == User.Role.COUPLE


@dataclass(frozen=True)
class SystemActor:
    """The seed command, the only caller allowed to act as the system (AD-3, AD-16)."""


SYSTEM = SystemActor()

# AD-3: the explicit `actor` every service takes.
Actor = GuestActor | AdminActor | SystemActor
