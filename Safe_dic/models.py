from django.db import models

# Create your models here.


# 创建用户表
class User(models.Model):
    username = models.CharField(max_length=80)
    api_key = models.CharField(max_length=40)

    class Meta:
        db_table = 'user'


# 创建访问控制表
class AccessControl(models.Model):
    serviceName = models.CharField(max_length=100)
    acl = models.CharField(max_length=100)
    WhiteName = models.CharField(max_length=100)

    class Meta:
        db_table = 'accesscontrol'


# 创建流量控制表
class FlowControl(models.Model):
    name = models.CharField(max_length=100, default='rate-limitin')
    username = models.CharField(max_length=100)
    serviceName = models.CharField(max_length=100)
    user_day =  models.IntegerField()


    class Meta:
        db_table = 'flowcontrol'

