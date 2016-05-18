# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20160516_0907'),
    ]

    operations = [
        migrations.CreateModel(
            name='Telefone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('ddd', models.DecimalField(decimal_places=0, blank=True, max_digits=3, default='051', null=True)),
                ('telefone', models.DecimalField(blank=True, decimal_places=0, max_digits=9, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='mandado',
            name='ddd',
        ),
        migrations.RemoveField(
            model_name='mandado',
            name='telefone',
        ),
        migrations.AlterField(
            model_name='documento',
            name='data',
            field=models.DateField(default=datetime.datetime(2016, 5, 17, 8, 50, 59, 26708)),
        ),
        migrations.AlterField(
            model_name='mandado',
            name='data',
            field=models.DateField(help_text='Data de recebimento.', default=datetime.date(2016, 5, 17)),
        ),
        migrations.AddField(
            model_name='telefone',
            name='mandado',
            field=models.ForeignKey(to='app.Mandado', related_name='telefone', blank=True, null=True),
        ),
    ]
