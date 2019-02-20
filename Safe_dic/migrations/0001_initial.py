# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessControl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('serviceName', models.CharField(max_length=100)),
                ('acl', models.CharField(max_length=100)),
                ('WhiteName', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'accesscontrol',
            },
        ),
        migrations.CreateModel(
            name='FlowControl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100, default='rate-limitin')),
                ('username', models.CharField(max_length=100)),
                ('serviceName', models.CharField(max_length=100)),
                ('user_day', models.IntegerField()),
            ],
            options={
                'db_table': 'flowcontrol',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('username', models.CharField(max_length=80)),
                ('api_key', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
