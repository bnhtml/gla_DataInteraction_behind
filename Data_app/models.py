from django.db import models

# Create your models here.


# 创建数据目录表
class DataName(models.Model):
    data_name = models.CharField(max_length=100)  # 数据目录名称
    domain_name = models.CharField(max_length=100)  # 域名
    first_name = models.CharField(max_length=100)  # 一级目录
    second_name = models.CharField(max_length=100)  # 二级目录
    third_name = models.CharField(max_length=100)  # 三级目录
    interface_type = models.CharField(max_length=100)  # 接口类型
    interface_name = models.CharField(max_length=800)  # 接口名称
    gender_choices = (
        (0, "exist"),
        (1, "delete"),
    )
    is_delete = models.IntegerField(choices=gender_choices, default=0)

    class Meta:
        db_table = 'dataname'