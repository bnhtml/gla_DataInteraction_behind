# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aacl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('serviceName', models.CharField(max_length=80)),
                ('name', models.CharField(max_length=80)),
                ('whitelist', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'Aacl',
            },
        ),
        migrations.CreateModel(
            name='Acontrols',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=80)),
                ('consumer_id', models.CharField(max_length=80)),
                ('day', models.CharField(max_length=80)),
                ('serviceName', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'Acontrols',
            },
        ),
        migrations.CreateModel(
            name='Agroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('group', models.CharField(max_length=80)),
                ('username', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'Agroup',
            },
        ),
        migrations.CreateModel(
            name='Aservice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('serviceName', models.CharField(max_length=80, unique=True)),
                ('hosts', models.CharField(max_length=80)),
                ('uris', models.CharField(max_length=80)),
                ('upstream_url', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'Aservice',
            },
        ),
        migrations.CreateModel(
            name='Auser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('username', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'Auser',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('dataname', models.CharField(max_length=80)),
                ('us_dataname', models.CharField(max_length=80)),
                ('hosts', models.CharField(max_length=80)),
                ('ogCode', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='GetDatalinkUrls',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('airTime', models.CharField(max_length=80)),
                ('department', models.CharField(max_length=80)),
                ('depUrl', models.CharField(max_length=80)),
                ('datalink_url', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'getDatalinkUrls',
            },
        ),
        migrations.CreateModel(
            name='HyParticipation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('airTime', models.CharField(max_length=80)),
                ('procId', models.CharField(max_length=80)),
                ('resourceId', models.CharField(max_length=80)),
                ('visitAverageCall', models.CharField(max_length=80)),
                ('isTransact', models.IntegerField()),
            ],
            options={
                'db_table': 'hyParticipation',
            },
        ),
        migrations.CreateModel(
            name='MyLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('superTask', models.CharField(max_length=100)),
                ('superObject', models.CharField(max_length=100)),
                ('superUser', models.CharField(max_length=100)),
                ('superAirtime', models.CharField(max_length=100)),
                ('superEndtime', models.CharField(max_length=100)),
                ('superStatus', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'mylog',
            },
        ),
        migrations.CreateModel(
            name='NoticeData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('airTime', models.CharField(max_length=80, unique=True)),
                ('resourceId', models.CharField(max_length=80)),
                ('type', models.CharField(max_length=80)),
                ('isTransact', models.IntegerField()),
            ],
            options={
                'db_table': 'noticedata',
            },
        ),
        migrations.CreateModel(
            name='ResourceTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('resourceName', models.CharField(max_length=100)),
                ('tableName', models.CharField(max_length=100)),
                ('databridgeName', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'resourcetable',
            },
        ),
        migrations.CreateModel(
            name='StaLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('staIP', models.CharField(max_length=100)),
                ('staTime', models.CharField(max_length=100)),
                ('staMethod', models.CharField(max_length=100)),
                ('staDataName', models.CharField(max_length=100)),
                ('staDataList', models.CharField(max_length=100)),
                ('staUser', models.CharField(max_length=100)),
                ('staStatus', models.CharField(max_length=100)),
                ('staDataSize', models.CharField(max_length=100)),
                ('staClient', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'stalog',
            },
        ),
        migrations.CreateModel(
            name='Uacl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('serviceName', models.CharField(max_length=80)),
                ('name', models.CharField(max_length=80)),
                ('whitelist', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'Uacl',
            },
        ),
        migrations.CreateModel(
            name='Ucontrols',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=80)),
                ('consumer_id', models.CharField(max_length=80)),
                ('day', models.CharField(max_length=80)),
                ('serviceName', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'Ucontrols',
            },
        ),
        migrations.CreateModel(
            name='Ugroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('group', models.CharField(max_length=80)),
                ('username', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'Ugroup',
            },
        ),
        migrations.CreateModel(
            name='Uservice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('serviceName', models.CharField(max_length=80, unique=True)),
                ('hosts', models.CharField(max_length=80)),
                ('uris', models.CharField(max_length=80)),
                ('client_type', models.CharField(max_length=80)),
                ('upstream_url', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'Uservice',
            },
        ),
        migrations.CreateModel(
            name='Uuser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('username', models.CharField(max_length=80, unique=True)),
                ('api_key', models.CharField(max_length=40)),
                ('depart', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Uuser',
            },
        ),
    ]
