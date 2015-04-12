from django.test import TestCase
from django_dynamic_fixture import G
from mock import patch

from crowdpact.apps.account.models import Account
from crowdpact.apps.event.models import (
    EmailNotification, Event, SiteNotification
)
from crowdpact.apps.event.processing import create_notifications_for_users, send_notifications


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

    def test_create_notifications_for_users_respects_account_email_preference(self):
        """
        Test that calling create_notifications_for_users will not create EmailNotification
        records for that event if the account does not want emails.
        """
        # Setup scenario
        act = G(Account, send_email_notifications=False)
        evt = G(Event, context={})

        # Run code
        create_notifications_for_users([act], evt)

        # Verify expectations
        self.assertFalse(EmailNotification.objects.filter(account=act, event=evt, sent=False).exists())
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
