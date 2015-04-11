from datetime import datetime

from django.test import TestCase, TransactionTestCase
from django_dynamic_fixture import G
from mock import patch

from crowdpact.apps.account.models import Account
from crowdpact.apps.event.models import Event
from crowdpact.apps.pact.models import Pact, Pledge


class PactTests(TestCase):
    def test_pledge_count(self):
        """
        Verify that the pledge_count property returns the total number of pledges for a Pact.
        """
        # Setup scenario
        pact = G(Pact, goal=10)
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

    @patch.object(Event, 'notify_users', spec_set=True)
    def test_pledge_creation_triggers_pact_success_when_goal_met(self, notify_users):
        """
        Verify that when we create the last pledge needed to meet a Pact's goal,
        the Pact is updated and an Event is created appropriately.
        """
        # Setup scenario
        pact = G(Pact, goal=2)

        # Verify initial assumptions
        self.assertEquals(0, Event.objects.count())

        # Run code
        G(Pledge, pact=pact)

        # Run code and verify expectations
        self.assertEqual(2, pact.pledge_count)
        self.assertTrue(Event.objects.filter(name='pact_goal_met').exists())
        self.assertEqual({
            'subject': 'Pact Succeeded!',
            'pact': pact.id,
            'met_goal': True,
        }, Event.objects.get(name='pact_goal_met').context)
        self.assertEquals(
            set(pact.pledge_set.values_list('pk')), set(notify_users.call_args_list[0][0][0].values_list('pk')))

    @patch.object(Event, 'notify_users', spec_set=True)
    def test_pledge_creation_does_not_trigger_pact_success_when_goal_not_met(self, notify_users):
        """
        Verify that when if a goal has already been met, we don't trigger success logic with further pledges.
        """
        # Setup scenario
        pact = G(Pact, goal=1, goal_met=True, notification_events_created=True)

        # Run code
        G(Pledge, pact=pact)

        # Run code and verify expectations
        self.assertEqual(2, pact.pledge_count)
        self.assertEquals(0, Event.objects.count())
        self.assertFalse(notify_users.called)

    @patch.object(Event, 'notify_users', spec_set=True)
    def test_pledge_creation_does_not_trigger_pact_success_when_goal_already_met(self, notify_users):
        """
        Verify that when if we create a last pledge the Pact success case is not triggered if we
        haven't yet met our goal.
        """
        # Setup scenario
        pact = G(Pact, goal=3)

        # Verify initial assumptions
        self.assertEquals(0, Event.objects.count())

        # Run code
        G(Pledge, pact=pact)

        # Run code and verify expectations
        self.assertEqual(2, pact.pledge_count)
        self.assertEquals(0, Event.objects.count())
        self.assertFalse(notify_users.called)


class PactTransactionTests(TransactionTestCase):
    def test_no_double_pledge(self):
        """
        Verify that a given user cannot double-pledge for the same pact.
        """
        # Setup scenario
        other_account = G(Account)

        pact = G(Pact, creator=G(Account), goal=10)

        # Run code
        p1 = pact.pledge(other_account)
        p2 = pact.pledge(other_account)

        # Verify expectations
        self.assertTrue(type(p1) is Pledge)
        self.assertIsNone(p2)
        self.assertEqual(2, Pledge.objects.filter(pact=pact).count())
