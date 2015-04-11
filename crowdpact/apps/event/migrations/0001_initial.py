# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent', models.BooleanField(default=False)),
                ('account', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('context', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='SiteNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('read', models.BooleanField(default=False)),
                ('account', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(to='event.Event')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='emailnotification',
            name='event',
            field=models.ForeignKey(to='event.Event'),
        ),
    ]
