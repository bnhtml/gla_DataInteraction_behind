# -*- coding: utf-8 -*
from django.conf.urls import include, url
from departAdmin import views

urlpatterns = [
    # url(r'^admin/$', views.admin),

    url(r'^admin_catalog/$', views.admin_catalog),  # 填写三级目录页面
    #  四大通道
    url(r'^db_list/$', views.db_list),  # db展示页面
    url(r'^admin_file/$', views.admin_file),  # 文件通道路由
    url(r'^admin_interface/$', views.admin_interface),  # 接口通道名称
    url(r'^admin_ways/$', views.admin_ways),  # 消息通道名称
    url(r'^page_Sql/$', views.page_Sql),  # 添加sql选项卡
    url(r'sql_admin/$', views.sql_admin),  # select语句生成页面
    url(r'^add_feild/$', views.add_feild), # 添加数据库字段
    url(r'^file_add/$', views.type_add), # 添加三大通道类型
    url(r'^update_type/$', views.update_type), # 修改三大通道类型
    url(r'^del_type/$', views.del_type), # 删除三大通道
    url(r'^add_table/$', views.add_table), # 管理员页面添加数据表操作
    url(r'^add_field/$', views.add_field),  # 管理员页面添加字段操作
    url(r'^field_show/$', views.field_show),  # 页面显示字段信息
    url(r'^get_table/$', views.get_table), # sql页面获取数据
    url(r'^table_delete/$', views.table_delete),  # 数据源删除数据表
    url(r'^field_delete/$', views.field_delete),  # 数据源删除字段操作
    url(r'^update_table/$', views.update_table),  # 数据源修改表名
    url(r'^update_field/$', views.update_field),  # 数据源修改字段
    url(r'^update_list/$', views.update_catalog),  # 三级目录修改操作
    url(r'^delete_list/$', views.delete_catalog),  # 三级目录删除操作
    url(r'^first_info/$', views.catalog_info),  # 获取一级目录信息
    url(r'^second_info/$', views.second_info),  # 获取二级目录信息
    url(r'^third_info/$', views.third_info),  # 获取三级目录信息
    url(r'^second_list/$', views.second_list),  # 二级目录展示到页面上
    url(r'^third_list/$', views.third_list),  # 三级目录战士到页面上
    url(r'^admin_catalog/$', views.admin_catalog),  # 填写三级目录页面
    url(r'^update_data/$',views.update_data),#sql写入文件
    url(r'^sql_append', views.sql_append),  # 生成sql页面
    url(r'^sql_save/$', views.sql_save),  # sql保存页面
    url(r'^sql_name/$', views.sql_name),  # 添加sql选项卡
    url(r'^sql_update/$', views.sql_update), # 更新sql语句
    url(r'^delete_db/$', views.delete_db),  # 删除sql语句

    url(r'^file_list/$', views.file_list),  # 文件源名称展示页面
    url(r'^interface_list/$', views.interface_list),  # 接口源名称展示页面
    url(r'^message_list/$', views.message_list),  # 消息源录入展示页面
    url(r'^meta_list/$', views.meta_list),  # 获取元数据参数
    url(r'^add_meta/$', views.add_meta),  # 添加元数据名称
    url(r'^add_params/$', views.add_params),  # 添加元数据参数
    url(r'^meta_update/$', views.meta_update),  # 修改数据元名称
    url(r'^params_update/$', views.params_update),  # 修改数据源参数
    url(r'^del_meta/$', views.del_meta),  # 删除数据源名称
    url(r'^del_params/$', views.del_params),  # 删除数据源参数
    url(r'^get_ftype/$', views.get_ftype),  # 获取字段类型
    url(r'^user_list/$', views.user_list),  # 获取用户列表
    url(r'^service_list/$', views.service_list),  # 获取数据接口封装
    url(r'^acl_list/$', views.acl_list),  # 获取访问控制
    url(r'^control_list/$', views.control_list),  # 获取流量控制

    url(r'^desc/(\w+)/$', views.desc_show),  # 查询所有表结构
    url(r'^(.*)/(\w+)/$', views.admin),


]
