# -*- coding: utf-8 -*
from django.conf.urls import include, url
from commonUser import views

urlpatterns = [
    url(r'^(.*)/(\w+)/$', views.index),
    url(r'^acl_list/$', views.acl_list),
    url(r'^control_list/$', views.control_list),
    url(r'^service_list/$', views.service_list),
    url(r'^user_operation/$', views.user_operation),  # 增删改查
    url(r'^service_type/$', views.service_type),  # 服务目录参数
    url(r'^update_service', views.update_service),  # 修改服务
    url(r'^update_acl/$', views.update_acl),  # 修改acl
    url(r'^update_control/$', views.update_control),  # 修改流量控制
    url(r'^select-checkbox/$', views.selectcheckbox),
    url(r'^user_getfirst/$', views.user_getfirst),  # 二级目录获取
    url(r'^user_getsecond/$', views.user_getsecond),  # 三级目录获取
    url(r'^user_getthird/$', views.user_getthird),  # 三级目录获取
    url(r'^get_chname/$', views.get_chname),  # 获取数据目录修改之前的三级目录值
    url(r'^page_nation/$', views.page_nation), # 分页
]
