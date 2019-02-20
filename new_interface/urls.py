# -*- coding: utf-8 -*

from django.conf.urls import url
from new_interface import views

urlpatterns = [
   url(r'^get_firstdir', views.get_firstdir),  # 获取一级目录
   url(r'^get_seconddir', views.get_seconddir),  # 获取二级目录
   url(r'^get_thirddir', views.get_thirddir),  # 获取三级目录
   url(r'^get_toldp', views.get_toldp),  # 获取全部部门
   url(r'^get_coundp', views.get_coundp), # 获取国家部门
   url(r'^get_prodp', views.get_prodp),  # 获取省直部门
   url(r'^get_citydp', views.get_citydp),  # 获取市州部门
   url(r'^conf_log', views.conf_log),  # 获取配置日志
   url(r'^getDone_interface$', views.getDone_interface),  #获取发布接口数据
   url(r'^getUnpublished_interface$', views.getUnpublished_interface),  #获取未发布接口数据
]
