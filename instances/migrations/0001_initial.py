# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import instances.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('label', instances.fields.DNSLabelField(unique=True, max_length=63, db_index=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(related_name='created_instances', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('users', models.ManyToManyField(related_name='instances', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
