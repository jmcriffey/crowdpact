from django.db import models
from django.template.loader import render_to_string

from jsonfield import JSONField

from crowdpact.apps.utils.email import send_email


class Notification(models.Model):
    account = models.ForeignKey('account.Account')
    event = models.ForeignKey('event.Event')

    class Meta:
        abstract = True


class SiteNotification(Notification):
    """
    This is a notification that should be viewed on the site.
    """
    read = models.BooleanField(default=False)

    def mark_read(self):
        self.read = True
        self.save(update_fields=['read'])


class EmailNotification(Notification):
    """
    This is a notification that should be sent via email.
    """
    sent = models.BooleanField(default=False)

    def send(self):
        """
        Send this email corresponding for this notification.
        """
        # Send the email
        recipients = [self.account.email]

        send_email(
            self.event.context['subject'], self.txt_message, 'donotreply@crowdpact.org', recipients,
            message_html=self.html_message)

        self.sent = True
        self.save(update_fields=['sent'])

    def _render_template(self, template_name):
        return render_to_string(template_name, self.event.context)

    @property
    def txt_message(self):
        return self._render_template('{0}_email.txt'.format(self.event.name))

    @property
    def html_message(self):
        return self._render_template('{0}_email.html'.format(self.event.name))


class Event(models.Model):
    """
    This model is used for tracking events that may be of interest to users.
    """
    name = models.TextField()
    context = JSONField()
