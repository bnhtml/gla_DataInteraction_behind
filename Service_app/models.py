from django.db import models

# Create your models here.


# 创建服务目录表
class ServiceData(models.Model):
    link_name = models.CharField(max_length=100)  # 域名
    firstName = models.CharField(max_length=100)  # 一级目录
    secondName = models.CharField(max_length=100)  # 二级目录
    thirdName = models.CharField(max_length=100)  # 三级目录
    gender_choices = (
        (0, "exist"),
        (1, "delete"),
    )
    is_delete = models.IntegerField(choices=gender_choices, default=0)

    class Meta:
        db_table = 'servicedata'