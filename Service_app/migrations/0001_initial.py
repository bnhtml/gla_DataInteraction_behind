# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('link_name', models.CharField(max_length=100)),
                ('firstName', models.CharField(max_length=100)),
                ('secondName', models.CharField(max_length=100)),
                ('thirdName', models.CharField(max_length=100)),
                ('is_delete', models.IntegerField(default=0, choices=[(0, 'exist'), (1, 'delete')])),
            ],
            options={
                'db_table': 'servicedata',
            },
        ),
    ]
