# -*- coding: utf-8 -*
from django.conf.urls import url
from controlCenter import views

urlpatterns = [
   url(r'^index/$', views.index),  # 控制台
   url(r'^dealed/$', views.isTransact),  # 办结
   url(r'^insert_mysql', views.insert_mysql),  # 数据目录信息插入中间库
   url(r'^tell_hy_successed', views.tell_hy_successed),  # 通知海云数据资源上架成功
   url(r'^commitFile', views.commitFile),  # 向海云提交文件
]
