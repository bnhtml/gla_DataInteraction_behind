# -*- coding: utf-8 -*
from django.conf.urls import url
from Data import views

urlpatterns = [
   url(r'^data_base/$', views.data_base),  # 查询所有库功能页面
   url(r'^desc/(.*)/$', views.desc_show),  # 查询所有表结构
   #url(r'^desc/(.*)/(.*)/(.*)/$', views.field_desc),  # 查询字段对应的表结构
   url(r'^server_list/$', views.server_list),  # 服务列表页面
   url(r'^name_type/$', views.name_type),  # 增加名称的页面
   url(r'^sql_server/$', views.sql_server),  # sql的页面
   url(r'^server_name/$', views.server_name),  # 显示服务名称的页面
   url(r'^file_server/$', views.file_server),  # 文件类型页面显示
   url(r'^message_server/$', views.message_server),  # 信息类型显示页面
   url(r'^interface_server/$', views.interface_server),  # 服务类型显示页面
   url(r'^first/$', views.getFirst),
   url(r'^first_(\d+)/$', views.getSecond),
   url(r'^second_(\d+)/(\d+)/$', views.getThird),
   url(r'^data_add/$', views.data_add), # 将添加的名称和类型用session存储
   url(r'^del_server/$', views.del_server),
   url(r'^file_name/$', views.file_name),  # 将添加的文件名称传给后端session存储
   url(r'^type_chose/$', views.type_chose),  # 通过判断类型选择上一步的页面
   url(r'^test/$', views.test),  # 测试代码页面
   url(r'^update_server_id/$', views.update_server_id),  # 修改服务id
   url(r'^update_server_name/$', views.update_server_name),  # 修改服务名称
   url(r'^page_Template/$', views.page_Template),  # 模版页面
   url(r'^submit_data/$', views.request_http),  # 数据上架


   # 接口测试
   url(r'^interface_test/$', views.interfaceTest),  # 借口测试页面
   # url(r'^add_user/$', views.integ_command),  # 增加用户
   # url(r'^del_user/$', views.integ_command),  # 删除用户
   # url(r'^add_server/$', views.add_server),  # 增加服务
   # url(r'^del_server1/$', views.del_server1),  # 删除服务
   # url(r'^add_group/$', views.add_group),  # 增加访问控制名单
   # url(r'^add_ACL/$', views.add_acl),  # 增加ACL
   # url(r'^del_ACL/$', views.del_acl),  # 删除ACL
   # url(r'^test11/$', views.test_test),
   # url(r'^add_control/$', views.add_control),  # 增加ACL
   # url(r'^del_conrrol/$', views.del_control),  # 删除ACL
   # url(r'^request_allocation/$', views.integ_command),  # 删除ACL
   # url(r'^interface_test1/$', views.interfaceTest1)
   url(r'^get_apikey/$', views.get_apikey)
]
