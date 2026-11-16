"""The one role check for admin writes (AD-10, FR-46).

Helper pages render read-only, but this check in the service is the protection.
"""

from wedding.actors import Actor, AdminActor
from wedding.services.exceptions import NotAllowed


def require_couple(actor: Actor) -> None:
    """AD-10, FR-46: raise `NotAllowed` unless `actor` is a couple account."""
    if not (isinstance(actor, AdminActor) and actor.is_couple):
        raise NotAllowed()
