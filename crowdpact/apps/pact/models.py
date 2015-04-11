from django.db import IntegrityError, models, transaction


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


class Pact(models.Model):
    """
    Represent a 'pact' that a group of people can agree to.
    """
    creator = models.ForeignKey('account.Account')
    name = models.TextField(unique=True)
    description = models.TextField()
    goal = models.IntegerField()
    deadline = models.DateTimeField()

    objects = PactManager()

    @property
    def pledge_count(self):
        """
        Return the number of pledges for this Pact.
        """
        return self.pledge_set.count()

    def pledge(self, user):
        """
        create a plege for this user for this pact.
        """
        try:
            return Pledge.objects.create(account=user, pact=self)
        except IntegrityError:
            transaction.rollback()
            return None

    def __unicode__(self):
        return u'{0} - {1} - {2}'.format(self.name, self.goal, self.deadline)

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
