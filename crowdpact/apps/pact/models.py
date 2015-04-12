from datetime import datetime

from django.db import IntegrityError, models, transaction
from django.db.models import Count
from pytz import utc as utc_tz

from crowdpact.apps.event.models import Event
from crowdpact.apps.event.processing import create_notifications_for_users, send_notifications


class PactManager(models.Manager):
    def pledged_for_user(self, user):
        """
        Return all of the Pacts pledged by this user (including the ones they created).
        """
        return self.filter(pledge__account=user)

    def created_by_user(self, user):
        """
        Return all of the Pacts created by this user.
        """
        return self.filter(creator=user)

    def get_most_popular(self):
        """
        Return the most popular Pacts by pledge count.
        """
        return Pact.objects.annotate(pledge_count_annotation=Count('pledge')).order_by('-pledge_count_annotation')

    def get_newest(self):
        """
        Return all packs ordered by newness.
        """
        return Pact.objects.order_by('-creation_time')

    def get_ending_soon(self):
        """
        Return all Pacts ordered by time deadline.
        """
        return Pact.objects.filter(deadline__gt=utc_tz.localize(datetime.utcnow())).order_by('deadline')

    def search(self, search_string, tokenize=False):
        """
        Provides an interface for searching for Pacts.
        """
        if tokenize:
            return self._search_for_terms(self._tokenize(search_string))
        else:
            return self._search_for_terms([search_string])

    def _tokenize(self, s):
        """
        Split a string along whitespace boundaries and strip surrounding whitespace.
        """
        return [w.strip() for w in s.split(' ')]

    def _search_for_terms(self, search_terms):
        """
        Search for any Pact's that contain the provided search terms.
        """
        matching_pacts = []

        for term in search_terms:
            pacts = list(Pact.objects.filter(models.Q(name__icontains=term) | models.Q(description__icontains=term)))
            if pacts:
                matching_pacts += pacts

        return matching_pacts


class Pact(models.Model):
    """
    Represent a 'pact' that a group of people can agree to.
    """
    creator = models.ForeignKey('account.Account')
    name = models.TextField(unique=True)
    description = models.TextField()
    goal = models.IntegerField()
    deadline = models.DateTimeField()
    creation_time = models.DateTimeField(auto_now_add=True)

    # State variables for handling the endgame
    goal_met = models.BooleanField(default=False)
    notification_events_created = models.BooleanField(default=False)

    objects = PactManager()

    @property
    def has_enough_pledges(self):
        """
        Does this Pact have enough pledges?
        """
        return self.pledge_count >= self.goal

    @property
    def pledge_count(self):
        """
        Return the number of pledges for this Pact.
        """
        return self.pledge_set.count()

    @property
    def is_ongoing(self):
        """
        Return if the pledge is still ongoing (ie, we've not hit the deadline).
        """
        return utc_tz.localize(datetime.utcnow()) < self.deadline

    def make_pledge(self, user):
        """
        create a plege for this user for this pact.
        """
        try:
            return Pledge.objects.create(account=user, pact=self)
        except IntegrityError:
            transaction.rollback()
            return None

    def set_goal_suceeded(self):
        """
        Handle the case where the Pact's goal was met.
        """
        self._set_goal_met()
        self._create_success_event()

    def _create_success_event(self):
        """
        Create the 'Success' event for all pledges.
        """
        evt = Event.objects.create(name='pact_goal_met', context={
            'subject': 'Pact Succeeded!',
            'pact': self.id,
            'met_goal': True,
        })

        create_notifications_for_users(self.pledge_set.all(), evt)
        self._set_notification_events_created()

        # NOTE: the below should eventually be in a periodic task
        send_notifications()

    def __unicode__(self):
        return u'{0} - {1} - {2}'.format(self.name, self.goal, self.deadline)

    # Save methods
    def _set_goal_met(self):
        self.goal_met = True
        self.save(update_fields=['goal_met'])

    def _set_notification_events_created(self):
        self.notification_events_created = True
        self.save(update_fields=['notification_events_created'])

    def save(self, *args, **kwargs):
        this_is_initial_save = not bool(getattr(self, 'id', None))

        super(Pact, self).save(*args, **kwargs)

        if this_is_initial_save:
            Pledge.objects.create(pact=self, account=self.creator)


class Pledge(models.Model):
    """
    A through model that connects a given user with a pact that they have pledged to.
    """
    account = models.ForeignKey('account.Account')
    pact = models.ForeignKey('pact.Pact')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('account', 'pact',)

    def __unicode__(self):
        return u'{0} {1}'.format(self.account.username, self.pact.name)

    def save(self, *args, **kwargs):
        super(Pledge, self).save(*args, **kwargs)

        if self.pact.has_enough_pledges and self.pact.is_ongoing:
            if not self.pact.goal_met:
                self.pact.set_goal_suceeded()
