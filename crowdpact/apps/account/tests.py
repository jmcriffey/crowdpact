from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from crowdpact.apps.account.models import Account


class AccountAPITests(APITestCase):
    def test_set_send_email_notifications(self):
        """
        Verify that we can change the email notifications settings via the API.
        """
        # Setup scenario
        username = 'tester'
        password = 'secret'
        user = Account.objects.create_user(username=username, email='john.snow@gmail.com', password=password)

        self.assertTrue(self.client.login(username=username, password=password))

        # Verify initial assumptions
        self.assertTrue(user.send_email_notifications)

        # Run code
        resp = self.client.post(reverse('account.api.configure_email'), {
            'send_email_notifications': False,
        }, format='json')

        # Verify expectations
        self.assertEquals(status.HTTP_201_CREATED, resp.status_code)
        self.assertTrue(user.send_email_notifications)
