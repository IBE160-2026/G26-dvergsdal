"""Who is acting: a guest, an admin user or the system (AD-3, AD-6, AD-10).

Every service takes one of these as an explicit `actor`, never the request, and
records it as the author of the write. A guest actor comes only from the resolver
in `wedding/links.py`; the system actor is used only by the seed command; the
operator actor only by the `create_admin` command (Story 3.1). This module only
describes actors and writes nothing.
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


@dataclass(frozen=True)
class OperatorActor:
    """The person at the server console running `create_admin` (FR-47, AD-3, AD-10).

    Story 3.1. It names the real caller of the command that makes real accounts,
    apart from the seed's system actor. `require_couple` refuses it, so it cannot
    write through any admin service.
    """


OPERATOR = OperatorActor()

# AD-3: the explicit `actor` every service takes.
Actor = GuestActor | AdminActor | SystemActor | OperatorActor
