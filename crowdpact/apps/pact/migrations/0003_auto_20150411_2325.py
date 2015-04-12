# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pact', '0002_auto_20150411_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='pact',
            name='goal_met',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pact',
            name='notification_events_created',
            field=models.BooleanField(default=False),
        ),
    ]
