# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20160517_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='data',
            field=models.DateField(default=datetime.datetime(2016, 5, 17, 9, 22, 42, 100704)),
        ),
        migrations.AlterField(
            model_name='telefone',
            name='ddd',
            field=models.CharField(blank=True, max_length=3, null=True, default='051'),
        ),
        migrations.AlterField(
            model_name='telefone',
            name='telefone',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
    ]
