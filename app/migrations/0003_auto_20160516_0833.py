# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160512_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='data',
            field=models.DateField(default=datetime.datetime(2016, 5, 16, 8, 33, 30, 964356)),
        ),
        migrations.AlterField(
            model_name='mandado',
            name='data',
            field=models.DateField(default=datetime.date(2016, 5, 16), help_text='Data de recebimento.'),
        ),
        migrations.AlterField(
            model_name='mandado',
            name='owner',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='mandados'),
        ),
    ]
