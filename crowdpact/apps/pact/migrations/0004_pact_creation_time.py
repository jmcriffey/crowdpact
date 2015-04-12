# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pact', '0003_auto_20150411_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='pact',
            name='creation_time',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0), auto_now_add=True),
            preserve_default=False,
        ),
    ]
