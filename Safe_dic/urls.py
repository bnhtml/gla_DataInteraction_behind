from django.conf.urls import url
from Safe_dic import views



urlpatterns = [
    # url(r'^save_list/$', views.save_list),  # 获取安全目录数据
    # url(r'^add_save/$', views.add_save),  # 添加安全目录数据
    # url(r'^del_save/$', views.del_save),  # 删除安全目录数据
    url(r'^findControl/(\w+)/$', views.findControl),  # 查询安全目录访问控制接口
    url(r'^findFlow/(\w+)/$', views.findFlow),  # 查询安全目录流控接口
    url(r'^findUser/(\w+)/$', views.findUser),  # 查询安全目录用户接口
]
