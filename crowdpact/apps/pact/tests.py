from datetime import datetime

from django.test import TestCase, TransactionTestCase
from django_dynamic_fixture import G

from crowdpact.apps.account.models import Account
from crowdpact.apps.pact.models import Pact, Pledge


class PactTests(TestCase):
    def test_pledge_count(self):
        """
        Verify that the pledge_count property returns the total number of pledges for a Pact.
        """
        # Setup scenario
        pact = G(Pact, creator=G(Account))
        G(Pledge, pact=pact)

        # Run code and verify expectations
        self.assertEqual(2, pact.pledge_count)

    def test_creator_is_pledge(self):
        """
        Verify that when a user creates a Pact, they are added as a pledge.
        """
        # Setup scenario
        act = G(Account)

        # Run code
        pact = Pact.objects.create(name='Test pact', creator=act, goal=3, deadline=datetime(2015, 1, 1))

        # Verify expectations
        self.assertEqual(1, Pledge.objects.filter(pact=pact).count())


class PactTransactionTests(TransactionTestCase):
    def test_no_double_pledge(self):
        """
        Verify that a given user cannot double-pledge for the same pact.
        """
        # Setup scenario
        creator = G(Account)
        other_account = G(Account)

        pact = G(Pact, creator=creator)

        # Run code
        p1 = pact.pledge(other_account)
        p2 = pact.pledge(other_account)

        # Verify expectations
        self.assertTrue(type(p1) is Pledge)
        self.assertIsNone(p2)
        self.assertEqual(2, Pledge.objects.filter(pact=pact).count())
