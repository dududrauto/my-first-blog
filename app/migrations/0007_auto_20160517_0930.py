# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20160517_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='telefone',
            name='oficial',
            field=models.ForeignKey(related_name='lista_telefones', help_text='Se em em branco, preenche automaticamente com o usuario atual.', null=True, blank=True, to='app.Oficial'),
        ),
        migrations.AlterField(
            model_name='documento',
            name='data',
            field=models.DateField(default=datetime.datetime(2016, 5, 17, 9, 30, 39, 957358)),
        ),
    ]
