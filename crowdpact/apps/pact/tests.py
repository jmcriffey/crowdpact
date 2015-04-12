from datetime import datetime

from django.test import TestCase, TransactionTestCase
from django_dynamic_fixture import G
from freezegun import freeze_time
from mock import patch
from pytz import utc as utc_tz

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

    @patch('crowdpact.apps.pact.models.send_notifications', spec_set=True)
    @patch('crowdpact.apps.pact.models.create_notifications_for_users', spec_set=True)
    def test_pledge_creation_triggers_pact_success_when_goal_met(
            self, create_notifications_for_users, send_notifications):
        """
        Verify that when we create the last pledge needed to meet a Pact's goal,
        the Pact is updated and an Event is created appropriately.
        """
        # Setup scenario
        now = utc_tz.localize(datetime(2015, 6, 1))
        deadline = utc_tz.localize(datetime(2015, 6, 6))
        pact = G(Pact, goal=2, deadline=deadline)

        # Verify initial assumptions
        self.assertEquals(0, Event.objects.count())

        # Run code
        with freeze_time(now):
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
            set(pact.pledge_set.values_list('pk')),
            set(create_notifications_for_users.call_args_list[0][0][0].values_list('pk')))
        self.assertEquals(1, send_notifications.call_count)

    @patch('crowdpact.apps.pact.models.send_notifications', spec_set=True)
    @patch('crowdpact.apps.pact.models.create_notifications_for_users', spec_set=True)
    def test_pledge_creation_does_not_trigger_pact_success_when_goal_not_met(
            self, create_notifications_for_users, send_notifications):
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
        self.assertFalse(create_notifications_for_users.called)
        self.assertFalse(send_notifications.called)

    @patch('crowdpact.apps.pact.models.send_notifications', spec_set=True)
    @patch('crowdpact.apps.pact.models.create_notifications_for_users', spec_set=True)
    def test_pledge_creation_does_not_trigger_pact_success_when_goal_already_met(
            self, create_notifications_for_users, send_notifications):
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
        self.assertFalse(create_notifications_for_users.called)
        self.assertFalse(send_notifications.called)

    @patch('crowdpact.apps.pact.models.send_notifications', spec_set=True)
    @patch('crowdpact.apps.pact.models.create_notifications_for_users', spec_set=True)
    def test_pledge_creation_does_not_trigger_pact_success_after_deadline(
            self, create_notifications_for_users, send_notifications):
        """
        Verify that when if we create a last pledge the Pact success case is not triggered if we
        haven't yet met our goal.
        """
        # Setup scenario
        pact = G(Pact, goal=1, deadline=utc_tz.localize(datetime(2000, 1, 1)))

        # Verify initial assumptions
        self.assertEquals(0, Event.objects.count())

        # Run code
        G(Pledge, pact=pact)

        # Run code and verify expectations
        self.assertEqual(2, pact.pledge_count)
        self.assertEquals(0, Event.objects.count())
        self.assertFalse(create_notifications_for_users.called)
        self.assertFalse(send_notifications.called)

    def test_search_for_one_term(self):
        # Setup scenario
        p1 = G(Pact, name='Vote for (Rand|Ron) Paul!')
        p2 = G(Pact, name='Vote for Ralph Nadir!')

        # Run code
        pacts = Pact.objects.search('vote', tokenize=True)

        # Verify expectations
        self.assertEquals(set([p1, p2]), set(pacts))

    def test_search_handles_no_results(self):
        # Setup scenario
        G(Pact, name='Vote for (Rand|Ron) Paul!')
        G(Pact, name='Vote for Ralph Nadir!')

        # Run code
        pacts = Pact.objects.search('Overthrow the proletariat!', tokenize=False)

        # Verify expectations
        self.assertEquals(set(), set(pacts))

    def test_search_for_tokenized_input_checks_names(self):
        # Setup scenario
        p1 = G(Pact, name='Vote for (Rand|Ron) Paul!')
        p2 = G(Pact, name='Vote for Ralph Nadir!')

        # Run code
        pacts = Pact.objects.search('ralph paul', tokenize=True)

        # Verify expectations
        self.assertEquals(set([p1, p2]), set(pacts))

    def test_search_for_non_tokenized_input_checks_names(self):
        # Setup scenario
        G(Pact, name='Vote for (Rand|Ron) Paul!')
        p1 = G(Pact, name='Vote for Ralph Nadir!')

        # Run code
        pacts = Pact.objects.search('Vote for Ralph', tokenize=False)

        # Verify expectations
        self.assertEquals([p1], pacts)

    def test_search_for_tokenized_input_checks_descriptions(self):
        # Setup scenario
        p1 = G(Pact, description='Vote for (Rand|Ron) Paul!')
        p2 = G(Pact, description='Vote for Ralph Nadir!')

        # Run code
        pacts = Pact.objects.search('ralph paul', tokenize=True)

        # Verify expectations
        self.assertEquals(set([p1, p2]), set(pacts))

    def test_search_for_non_tokenized_input_checks_descriptions(self):
        # Setup scenario
        G(Pact, description='Vote for (Rand|Ron) Paul!')
        p1 = G(Pact, description='Vote for Ralph Nadir!')

        # Run code
        pacts = Pact.objects.search('Vote for Ralph', tokenize=False)

        # Verify expectations
        self.assertEquals([p1], pacts)

    def test_most_popular(self):
        # Setup scenario
        a1 = G(Account)
        a2 = G(Account)

        # p1 will have 3 pledges
        p1 = G(Pact)
        # p2 will have 2 pledges
        p2 = G(Pact)
        # p2 will have 1 pledge
        p3 = G(Pact)

        p1.make_pledge(a1)
        p1.make_pledge(a2)

        p2.make_pledge(a1)

        # Run code
        most_popular = Pact.objects.get_most_popular()

        # Verify expectations
        self.assertEquals([p1, p2, p3], list(most_popular))


class PactTransactionTests(TransactionTestCase):
    def test_no_double_pledge(self):
        """
        Verify that a given user cannot double-pledge for the same pact.
        """
        # Setup scenario
        other_account = G(Account)

        pact = G(Pact, creator=G(Account), goal=10)

        # Run code
        p1 = pact.make_pledge(other_account)
        p2 = pact.make_pledge(other_account)

        # Verify expectations
        self.assertTrue(type(p1) is Pledge)
        self.assertIsNone(p2)
        self.assertEqual(2, Pledge.objects.filter(pact=pact).count())
