"""DataSheleves URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from superAdmin import views

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^data/', include('Data.urls')),
    url(r'^save/', include('Safe_dic.urls')),
    url(r'^controlCenter/', include('controlCenter.urls')),
    url(r'^commonUser/', include('commonUser.urls')),
    url(r'^departAdmin/', include('departAdmin.urls')),
    url(r'^new_interface/', include('new_interface.urls')),  # 新接口与vue前端交互
    url(r'^get_data/$', views.get_data_log),
    url(r'^api/getlog/$', views.get_data),
    url(r'^api/check_user_apikey/$', views.request_apikey),
    url(r'^api/userGroupApikey/$', views.userGroupApikey),
    url(r'^api/ogCodeURl/$', views.ogCodeURl),  # 单点登录url
    url(r'^api/test/$', views.content),  # 测试
    url(r'^api/haiyunDatalink/$', views.haiyunDatalink),  # 测试海云haiyunDatalink
    url(r'^api/achieveParticipation/$', views.AchieveParticipation),  # 海云入参
    url(r'^api/datalink/$', views.datalink),
    url(r'^api/getNotice/$', views.getNotice),  # 中软通知接口
    url(r'^api/getDatalinkUrls', views.getDatalinkUrls),  # 获取数据上架平台访问地址接口
    url(r'^service/', include('Service_app.urls')),  # 服务目录查询接口
    url(r'^dataFind/', include('Data_app.urls')),  # 数据目录查询接口
    url(r'^', include('superAdmin.urls')),
    url(r'^resources/server/login/$',views.serverLogin)
]
