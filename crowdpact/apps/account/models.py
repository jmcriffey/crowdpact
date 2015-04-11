from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class Account(PermissionsMixin, AbstractBaseUser):
    """
    Custom user model for a given user of crowdpact.
    """
    # Required fields
    username = models.TextField(unique=True)
    email = models.EmailField('email address')

    # Optional fields
    human_name = models.TextField(null=True, blank=True, default=None)
    about = models.TextField(null=True, blank=True, default=None)
    location = models.TextField(null=True, blank=True, default=None)
    website = models.URLField(null=True, blank=True, default=None)
    photo = models.TextField(null=True, blank=True, default=None)

    # Auto fields
    date_joined = models.DateTimeField(auto_now_add=True)

    # Required by Django
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return u'{0}'.format(self.username)
