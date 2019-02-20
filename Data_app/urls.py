# -*- coding: utf-8 -*
from django.conf.urls import  url
from Data_app import views


urlpatterns = [
  url(r'^data/(\w+)/$', views.findData),  # 数据目录查询接口
]