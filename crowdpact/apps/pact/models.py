from django.db import models


class Pact(models.Model):
    """
    Represent a 'pact' that a group of people can agree to.
    """
    creator = models.ForeignKey('account.Account')
    name = models.TextField(unique=True)
    description = models.TextField()
    goal = models.IntegerField()
    deadline = models.DateTimeField()

    def __unicode__(self):
        return u'{0} - {1} - {2}'.format(self.name, self.goal, self.deadline)


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
