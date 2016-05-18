# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20160516_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='data',
            field=models.DateField(default=datetime.datetime(2016, 5, 16, 9, 7, 17, 355470)),
        ),
        migrations.AlterField(
            model_name='mandado',
            name='owner',
            field=models.ForeignKey(related_name='mands', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
