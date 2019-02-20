# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('data_name', models.CharField(max_length=100)),
                ('domain_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('second_name', models.CharField(max_length=100)),
                ('third_name', models.CharField(max_length=100)),
                ('interface_type', models.CharField(max_length=100)),
                ('interface_name', models.CharField(max_length=800)),
                ('is_delete', models.IntegerField(default=0, choices=[(0, 'exist'), (1, 'delete')])),
            ],
            options={
                'db_table': 'dataname',
            },
        ),
    ]
