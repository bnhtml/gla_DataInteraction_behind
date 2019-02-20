# -*- coding: utf-8 -*
from django.conf.urls import  url
from Service_app import views

urlpatterns = [
   url('r^find/(\w+)/$', views.serviceFind),

]

