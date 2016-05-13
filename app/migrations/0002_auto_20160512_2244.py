# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='data',
            field=models.DateField(default=datetime.datetime(2016, 5, 12, 22, 44, 53, 603620)),
        ),
    ]
