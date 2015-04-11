from django.test import TestCase
from django_dynamic_fixture import G
from mock import patch

from crowdpact.apps.account.models import Account
from crowdpact.apps.event.models import (
    EmailNotification, Event, SiteNotification, create_notifications_for_users, send_notifications
)


class EventTests(TestCase):
    def test_create_notifications_for_users(self):
        """
        Test that calling create_notifications_for_users will create EmailNotification and SiteNotification
        records for that event and for each provided user.
        """
        # Setup scenario
        act = G(Account)
        evt = G(Event, context={})

        # Run code
        create_notifications_for_users([act], evt)

        # Verify expectations
        self.assertTrue(EmailNotification.objects.filter(account=act, event=evt, sent=False).exists())
        self.assertTrue(SiteNotification.objects.filter(account=act, event=evt, read=False).exists())

    @patch.object(EmailNotification, 'send', spec_set=True)
    def test_send_notifications(self, send):
        # Setup scenario
        act = G(Account)
        evt = G(Event, context={})
        G(EmailNotification, account=act, event=evt)

        # Run code
        send_notifications()

        # Verify expectations
        self.assertEquals(1, send.call_count)

    @patch('crowdpact.apps.event.models.send_notifications', spec_set=True)
    @patch('crowdpact.apps.event.models.create_notifications_for_users', spec_set=True)
    def test_notify_users(self, create_nofications_for_users, send_notifications):
        # Setup scenario
        act = G(Account)
        evt = G(Event, context={})

        # Run code
        evt.notify_users([act])

        # Verify expectations
        create_nofications_for_users.assert_called_with([act], evt)
        self.assertTrue(send_notifications.called)
