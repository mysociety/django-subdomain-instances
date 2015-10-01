# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import instances.fields


class Migration(migrations.Migration):

    dependencies = [
        ('instances', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instance',
            options={'verbose_name': 'instance', 'verbose_name_plural': 'instances'},
        ),
        migrations.AlterField(
            model_name='instance',
            name='created_by',
            field=models.ForeignKey(related_name='created_instances', verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='instance',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
        ),
        migrations.AlterField(
            model_name='instance',
            name='label',
            field=instances.fields.DNSLabelField(unique=True, max_length=63, verbose_name='label', db_index=True),
        ),
        migrations.AlterField(
            model_name='instance',
            name='title',
            field=models.CharField(max_length=100, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='instance',
            name='users',
            field=models.ManyToManyField(related_name='instances', verbose_name='users', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
