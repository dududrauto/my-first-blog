# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import tinymce.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Atendimento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('dia', models.DateField()),
                ('horario', models.TimeField(verbose_name='das')),
                ('fim', models.TimeField(verbose_name='às')),
            ],
        ),
        migrations.CreateModel(
            name='Aviso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('aviso', tinymce.models.HTMLField(default='Aqui será inserido automaticamente para mandados relacionados!')),
                ('data_aviso', models.DateField(auto_now=True)),
                ('atendimento', models.ForeignKey(to='app.Atendimento')),
            ],
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('documento', tinymce.models.HTMLField()),
                ('data', models.DateField(default=datetime.datetime(2016, 5, 12, 22, 44, 28, 3519))),
                ('atendimento', models.ForeignKey(null=True, blank=True, to='app.Atendimento')),
            ],
        ),
        migrations.CreateModel(
            name='Mandado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('comarca', models.DecimalField(default='003', decimal_places=0, max_digits=3)),
                ('vara', models.CharField(null=True, max_length=20, blank=True)),
                ('processo', models.DecimalField(null=True, decimal_places=0, blank=True, max_digits=20)),
                ('conducao', models.CharField(default='AJG', max_length=4, blank=True, null=True, verbose_name='Condução', choices=[('AJG', 'Assistência Judiciária Gratuita'), ('OK', 'Recolhida Vinculada'), ('PAGA', 'Falta Vincular'), ('NO', 'Não Paga')])),
                ('ano_mandado', models.CharField(default='2016', max_length=4)),
                ('numero_mandado', models.CharField(max_length=8)),
                ('n_mandado', models.IntegerField(unique=True, verbose_name='Número do Mandado')),
                ('data', models.DateField(default=datetime.date(2016, 5, 12), help_text='Data de recebimento.')),
                ('audiencia', models.DateField(null=True, blank=True)),
                ('destinatario', models.CharField(max_length=100)),
                ('ddd', models.CharField(default='051', max_length=3)),
                ('telefone', models.CharField(null=True, max_length=9, blank=True)),
                ('cep', models.CharField(help_text='Alternativamente, preencha "Campos de Endereço".', max_length=9, blank=True, null=True)),
                ('pais', models.CharField(default='Brasil', max_length=50)),
                ('estado', models.CharField(default='Rio Grande do Sul', max_length=50)),
                ('cidade', models.CharField(max_length=50)),
                ('bairro', models.CharField(null=True, max_length=50, blank=True)),
                ('rua', models.CharField(null=True, max_length=100, blank=True)),
                ('numero_rua', models.CharField(max_length=6, verbose_name='Número da Casa')),
                ('complemento', models.CharField(null=True, max_length=20, blank=True)),
                ('latitude', models.CharField(null=True, max_length=30, blank=True)),
                ('longitude', models.CharField(null=True, max_length=30, blank=True)),
                ('status_cumprimento', models.CharField(default='pu', max_length=2, choices=[('rd', 'Urgente'), ('gr', '$'), ('pu', 'Normal'), ('AV', 'Avidado'), ('DV', 'Devolvido'), ('CE', 'Certificar')], verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Modelo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nome', models.CharField(max_length=50)),
                ('modelo', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='Oficial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('telefone', models.DecimalField(max_digits=10, decimal_places=0)),
                ('usuario', models.ForeignKey(unique=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ordem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('tipo', models.CharField(max_length=10)),
                ('modelo', models.ForeignKey(to='app.Modelo')),
            ],
        ),
        migrations.AddField(
            model_name='mandado',
            name='oficial',
            field=models.ForeignKey(null=True, blank=True, help_text='Se em em branco, preenche automaticamente com o usuario atual.', to='app.Oficial', related_name='mandados'),
        ),
        migrations.AddField(
            model_name='mandado',
            name='ordem',
            field=models.ForeignKey(default=2, help_text='Citacao, Intimacao, Penhora, Avaliacao, Busca e Ap, etc...', to='app.Ordem'),
        ),
        migrations.AddField(
            model_name='mandado',
            name='owner',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='snippets'),
        ),
        migrations.AddField(
            model_name='documento',
            name='mandado',
            field=models.ForeignKey(to='app.Mandado'),
        ),
        migrations.AddField(
            model_name='documento',
            name='modelo',
            field=models.ForeignKey(to='app.Modelo'),
        ),
        migrations.AddField(
            model_name='documento',
            name='oficial',
            field=models.ForeignKey(to='app.Oficial'),
        ),
        migrations.AddField(
            model_name='aviso',
            name='oficial',
            field=models.ForeignKey(to='app.Oficial'),
        ),
        migrations.AddField(
            model_name='atendimento',
            name='oficial',
            field=models.ForeignKey(to='app.Oficial'),
        ),
    ]
