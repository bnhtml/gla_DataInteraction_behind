from django.db import models

# Create your models here.
from django.db import models


class ServerDict(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    top_class = models.CharField(max_length=300, default='')
    type = models.CharField(max_length=200)
    server_name = models.TextField()
    data_name = models.TextField()
    gender_choices = (
        (0, "exist"),
        (1, "delete"),
    )
    is_delete = models.IntegerField(choices=gender_choices, default=0)

    class Meta:
        db_table = 'serverdict'


class First(models.Model):

    id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=100)
    gender_choices = (
        (0, "exist"),
        (1, "delete"),
    )
    chinese_abb = models.CharField(max_length=80, default='')
    is_delete = models.IntegerField(choices=gender_choices, default=0,)

    class Meta:
        db_table = 'first'


class Second(models.Model):

    id = models.AutoField(primary_key=True)
    industry = models.CharField(max_length=100)
    first = models.ForeignKey(to="First",to_field="id",on_delete=True)
    gender_choices = (
        (0, "exist"),
        (1, "delete"),
    )
    chinese_abb = models.CharField(max_length=80, default='')
    is_delete = models.IntegerField(choices=gender_choices, default=0)

    class Meta:
        db_table = 'second'


class Third(models.Model):

    id = models.AutoField(primary_key=True)
    species = models.CharField(max_length=100)
    gender_choices = (
        (0, "exist"),
        (1, "delete"),
    )
    chinese_abb = models.CharField(max_length=80, default='')
    is_delete = models.IntegerField(choices=gender_choices, default=0)

    second = models.ForeignKey(to="Second",to_field="id",on_delete=True)

    first = models.ForeignKey(to="First",to_field="id",on_delete=True)

    class Meta:
        db_table = 'third'



class SaveTable(models.Model):
    id = models.AutoField(primary_key=True)
    tableName=models.CharField(max_length=80)
    class Meta:
        db_table = 'savetable'


class AddField(models.Model):
    id = models.AutoField(primary_key=True)
    fieldName=models.CharField(max_length=80)
    fieldDesc=models.CharField(max_length=80)
    fieldType=models.CharField(max_length=80)
    fieldKey=models.CharField(max_length=80)
    tableKey = models.ForeignKey(to="SaveTable", to_field="id", on_delete=True)
    is_delete = models.CharField(max_length=80)
    class Meta:
        db_table = 'add_field'