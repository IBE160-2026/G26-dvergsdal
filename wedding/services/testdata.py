"""Removing the test data the seed command made, so it can run again (FR-72, AD-4, AD-16).

Only rows marked `is_test_data` are removed: households, with everything in
them (also a guest added to one later), and admin users. Households and users
the seed did not make are never removed.
"""

from django.db import transaction

from wedding.actors import Actor, SystemActor
from wedding.models import Household, User
from wedding.services.exceptions import NotAllowed


def reset_test_data(actor: Actor) -> None:
    """FR-72, AD-3, AD-4, AD-16: delete every test household, its guests and every test user.

    Only the system actor may reset. Story 5.2 adds seeded payments; AD-4 forbids
    deleting a household with payments, so that story makes this service void the
    test households' payments first.
    """
    with transaction.atomic():
        if not isinstance(actor, SystemActor):
            raise NotAllowed()
        Household.objects.filter(is_test_data=True).delete()
        User.objects.filter(is_test_data=True).delete()
