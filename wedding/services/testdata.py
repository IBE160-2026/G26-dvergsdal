"""Removing the test data the seed command made, so it can run again (FR-72, AD-4, AD-16).

Only rows marked `is_test_data` are removed: households, with everything in
them (also a guest added to one later), and admin users. Households and users
the seed did not make are never removed. Story 2.6d: the test households'
answer `Submission` rows go first, since `Submission.object_id` is a plain id
that does not cascade (AD-4, AD-20).
"""

from django.db import transaction

from wedding.actors import Actor, SystemActor
from wedding.models import Household, HouseholdAnswer, Submission, User
from wedding.services.exceptions import NotAllowed


def reset_test_data(actor: Actor) -> None:
    """FR-72, AD-3, AD-4, AD-16: delete every test household, its guests and every test user.

    Only the system actor may reset. Story 5.2 adds seeded payments; AD-4 forbids
    deleting a household with payments, so that story makes this service void the
    test households' payments first. Story 2.6d (AD-20): the `Submission` rows
    that point at a test household's answer are deleted first; real ones stay.
    """
    with transaction.atomic():
        if not isinstance(actor, SystemActor):
            raise NotAllowed()
        test_answers = HouseholdAnswer.objects.filter(household__is_test_data=True)
        Submission.objects.filter(
            kind=Submission.ANSWER, object_id__in=test_answers.values("pk")
        ).delete()
        Household.objects.filter(is_test_data=True).delete()
        User.objects.filter(is_test_data=True).delete()
