# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddField',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fieldName', models.CharField(max_length=80)),
                ('fieldDesc', models.CharField(max_length=80)),
                ('fieldType', models.CharField(max_length=80)),
                ('fieldKey', models.CharField(max_length=80)),
                ('is_delete', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'add_field',
            },
        ),
        migrations.CreateModel(
            name='First',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('department', models.CharField(max_length=100)),
                ('chinese_abb', models.CharField(max_length=80, default='')),
                ('is_delete', models.IntegerField(default=0, choices=[(0, 'exist'), (1, 'delete')])),
            ],
            options={
                'db_table': 'first',
            },
        ),
        migrations.CreateModel(
            name='SaveTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tableName', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'savetable',
            },
        ),
        migrations.CreateModel(
            name='Second',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('industry', models.CharField(max_length=100)),
                ('chinese_abb', models.CharField(max_length=80, default='')),
                ('is_delete', models.IntegerField(default=0, choices=[(0, 'exist'), (1, 'delete')])),
                ('first', models.ForeignKey(on_delete=True, to='Data.First')),
            ],
            options={
                'db_table': 'second',
            },
        ),
        migrations.CreateModel(
            name='ServerDict',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('top_class', models.CharField(max_length=300, default='')),
                ('type', models.CharField(max_length=200)),
                ('server_name', models.TextField()),
                ('data_name', models.TextField()),
                ('is_delete', models.IntegerField(default=0, choices=[(0, 'exist'), (1, 'delete')])),
            ],
            options={
                'db_table': 'serverdict',
            },
        ),
        migrations.CreateModel(
            name='Third',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('species', models.CharField(max_length=100)),
                ('chinese_abb', models.CharField(max_length=80, default='')),
                ('is_delete', models.IntegerField(default=0, choices=[(0, 'exist'), (1, 'delete')])),
                ('first', models.ForeignKey(on_delete=True, to='Data.First')),
                ('second', models.ForeignKey(on_delete=True, to='Data.Second')),
            ],
            options={
                'db_table': 'third',
            },
        ),
        migrations.AddField(
            model_name='addfield',
            name='tableKey',
            field=models.ForeignKey(on_delete=True, to='Data.SaveTable'),
        ),
    ]
