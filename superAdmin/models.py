from django.db import models
from Data.models import First

# Create your models here.

from django.db import models

# Create your models here.


# 用户模型类
# 用户表
#class User(models.Model):
#    username = models.CharField(max_length=80)
#    user_id = models.CharField(max_length=80)
#    api_key = models.CharField(max_length=40)
#    first_id = models.ForeignKey('Data.First', on_delete=True)
#    create_time = models.DateTimeField
#
#    class Meta:
#        db_table = 'user'
#

#class ServerInfo(models.Model):
 #   DataName = models.CharField(max_length=200)
  #  UserId = models.ForeignKey('User', on_delete=True)


# 接口
# 管理员用户表
class Auser(models.Model):
    username = models.CharField(max_length=80, null=False)

    class Meta:
        db_table = 'Auser'


# 管理员访问控制用户组表
class Agroup(models.Model):
    group = models.CharField(max_length=80)
    username = models.CharField(max_length=80, null=False)

    class Meta:
        db_table = 'Agroup'


# 管理员服务表
class Aservice(models.Model):
    serviceName = models.CharField(max_length=80, null=False, unique=True)
    hosts = models.CharField(max_length=80, null=False)
    uris = models.CharField(max_length=80, null=False)
    upstream_url = models.CharField(max_length=80, null=False)

    class Meta:
        db_table = 'Aservice'


# 管理员ACL表
class Aacl(models.Model):
    serviceName = models.CharField(max_length=80, null=False)
    name = models.CharField(max_length=80, null=False)
    whitelist = models.CharField(max_length=80, null=False)

    class Meta:
        db_table = 'Aacl'


# 管理员流控表
class Acontrols(models.Model):
    name = models.CharField(max_length=80)
    consumer_id = models.CharField(max_length=80, null=False)
    day = models.CharField(max_length=80, null=False)
    serviceName = models.CharField(max_length=80, null=False)

    class Meta:
        db_table = 'Acontrols'


# 用户用户表
class Uuser(models.Model):
    username = models.CharField(max_length=80, null=False, unique=True)
    api_key = models.CharField(max_length=40, null=False)
    depart = models.CharField(max_length=100)

    class Meta:
        db_table = 'Uuser'


# 用户访问控制用户组表
class Ugroup(models.Model):
    group = models.CharField(max_length=80)
    username = models.CharField(max_length=80, null=False)

    class Meta:
        db_table = 'Ugroup'


# 用户服务表
class Uservice(models.Model):
    serviceName = models.CharField(max_length=80, null=False, unique=True)
    hosts = models.CharField(max_length=80, null=False)
    uris = models.CharField(max_length=80, null=False)
    client_type = models.CharField(max_length=80, null=False)
    upstream_url = models.CharField(max_length=80, null=False)

    class Meta:
        db_table = 'Uservice'


# 用户acl
class Uacl(models.Model):
    serviceName = models.CharField(max_length=80, null=False)
    name = models.CharField(max_length=80, null=False)
    whitelist = models.CharField(max_length=80, null=False)

    class Meta:
        db_table = 'Uacl'


# 用户流量控制表
class Ucontrols(models.Model):
    name = models.CharField(max_length=80)
    consumer_id = models.CharField(max_length=80, null=False)
    day = models.CharField(max_length=80, null=False)
    serviceName = models.CharField(max_length=80, null=False)

    class Meta:
        db_table = 'Ucontrols'


class Department(models.Model):
    dataname = models.CharField(max_length=80)
    us_dataname = models.CharField(max_length=80)
    hosts = models.CharField(max_length=80)
    ogCode = models.CharField(max_length=100)

    class Meta:
        db_table = 'department'


class MyLog(models.Model):

    superTask = models.CharField(max_length=100)
    superObject = models.CharField(max_length=100)
    superUser = models.CharField(max_length=100)
    superAirtime = models.CharField(max_length=100)
    superEndtime = models.CharField(max_length=100)
    superStatus = models.CharField(max_length=100)


    class Meta:
        db_table = 'mylog'


class StaLog(models.Model):

    staIP = models.CharField(max_length=100)
    staTime = models.CharField(max_length=100)
    staMethod = models.CharField(max_length=100)
    staDataName=models.CharField(max_length=100)
    staDataList = models.CharField(max_length=100)
    staUser = models.CharField(max_length=100)
    staStatus = models.CharField(max_length=100)
    staDataSize = models.CharField(max_length=100)
    staClient = models.CharField(max_length=100)


    class Meta:
        db_table = 'stalog'


# class BasicInter(models.Model):
#     hosts = models.CharField(max_length=80)
#     ogCode = models.CharField(max_length=100)
#     gender_choices = (
#         (0, "exist"),
#         (1, "delete"),
#     )
#     is_delete = models.IntegerField(choices=gender_choices, default=0)
#
#     class Meta:
#         db_table = 'BasicInter'


class ResourceTable(models.Model):
    resourceName = models.CharField(max_length=100)
    tableName = models.CharField(max_length=100)
    databridgeName = models.CharField(max_length=100)

    class Meta:
        db_table = 'resourcetable'


# class FileName(models.Model):
#     id = models.AutoField(primary_key=True)
#     file_name = models.CharField(max_length=100)
#
#     class Meta:
#         db_table = 'fileName'
#
#
# class FileParams(models.Model):
#     id = models.AutoField(primary_key=True)
#     file_name = models.CharField(max_length=200)
#     file_desc = models.CharField(max_length=200)
#     file_type = models.CharField(max_length=200)
#     filename_id = models.ForeignKey(to="FileName", to_field="id", on_delete=True)
#
#     class Meta:
#         db_table = 'fileParams'
#
#
# class InterfaceName(models.Model):
#     id = models.AutoField(primary_key=True)
#     interface_name = models.CharField(max_length=100)
#
#     class Meta:
#         db_table = 'interfaceName'
#
#
# class InterfaceParams(models.Model):
#     id = models.AutoField(primary_key=True)
#     interface_name = models.CharField(max_length=200)
#     interface_desc = models.CharField(max_length=200)
#     interface_type = models.CharField(max_length=200)
#     interface_id = models.ForeignKey(to="InterfaceName", to_field="id", on_delete=True)
#
#     class Meta:
#         db_table = 'interfaceParams'
#
#
# class MessageName(models.Model):
#     id = models.AutoField(primary_key=True)
#     message_name = models.CharField(max_length=100)
#
#     class Meta:
#         db_table = 'messageName'
#
#
# class MessageParams(models.Model):
#     id = models.AutoField(primary_key=True)
#     message_name = models.CharField(max_length=200)
#     message_desc = models.CharField(max_length=200)
#     message_type = models.CharField(max_length=200)
#     message_id = models.ForeignKey(to="MessageName", to_field="id", on_delete=True)
#
#     class Meta:
#         db_table = 'messageParams'

# 中软通知数据表
class NoticeData(models.Model):
    airTime = models.CharField(max_length=80, null=False, unique=True)
    resourceId = models.CharField(max_length=80, null=False)
    type = models.CharField(max_length=80, null=False)
    isTransact = models.IntegerField(null=False)

    class Meta:
        db_table = 'noticedata'


# 海云获取数据上架地址记录表
class GetDatalinkUrls(models.Model):
    airTime = models.CharField(max_length=80, null=False)
    department = models.CharField(max_length=80, null=False)
    depUrl = models.CharField(max_length=80, null=False)
    datalink_url = models.CharField(max_length=80, null=False)

    class Meta:
        db_table = 'getDatalinkUrls'


# 海云入参记录表
class HyParticipation(models.Model):
    airTime = models.CharField(max_length=80, null=False,)
    procId = models.CharField(max_length=80, null=False,)
    resourceId = models.CharField(max_length=80, null=False)
    visitAverageCall = models.CharField(max_length=80, null=False)
    isTransact = models.IntegerField(null=False)

    class Meta:
        db_table = 'hyParticipation'
