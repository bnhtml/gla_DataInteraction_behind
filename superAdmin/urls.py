# -*- coding: utf-8 -*

from django.conf.urls import url
from superAdmin import views



urlpatterns = [
    url(r'^login/$', views.login),
   # url(r'^login_check/$', views.login_check),
   # url(r'^user_manger/$', views.user_manger),
   # url(r'^auth_manger/$', views.auth_manger),
   # url(r'^server_info/$', views.server_info),
   # url(r'^server_safe/$', views.server_safe),
   # url(r'^onlylook/$', views.only_look),
    #　用户页面
    url(r'^user_list/$', views.user_list),
    url(r'^group_list/$', views.group_list),
    url(r'^control_list/$', views.control_list),
    url(r'^service_list/$', views.service_list),
    url(r'^acl_list/$', views.acl_list),
    # 管理员页面
    url(r'^admin/$', views.admin),
    url(r'^add_aepart/$', views.add_depart),
    # url(r'^admin_user/$', views.admin_user),
    # url(r'^admin_group/$', views.admin_group),
    # url(r'^admin_control/$', views.admin_control),
    # url(r'^admin_service/$', views.admin_service),
    # url(r'^admin_acl/$', views.admin_acl),
    url(r'^admin_operation/$', views.admin_operation),  # 操作基础数据
    url(r'^admin_db/$', views.admin_db),  # 数据库选择传入
    url(r'^admin_catalog/$', views.admin_catalog),  # 填写三级目录页面
    url(r'^admin_mapping/$', views.admin_mapping),  # 映射目录显示页面
    url(r'^first_info/$', views.catalog_info),  # 获取一级目录信息
    url(r'^second_info/$', views.second_info),  # 获取二级目录信息
    url(r'^third_info/$', views.third_info),  # 获取三级目录信息
    url(r'^second_list/$', views.second_list),  # 二级目录展示到页面上
    url(r'^third_list/$', views.third_list),  # 三级目录战士到页面上
    url(r'^delete_list/$', views.delete_catalog),  # 三级目录删除操作
    url(r'^update_list/$', views.update_catalog),  # 三级目录修改操作
    url(r'^realm/$',views.realm),  # 映射域名
    # 用户管理接入

    url(r'^login_data/$', views.user_login),  # 用户操作数据
    url(r'^user_operation/$', views.user_operation),
    url(r'^welcome/$', views.welcome),
    url(r'^user_getfirst/$', views.user_getfirst),  # 二级目录获取
    url(r'^user_getsecond/$', views.user_getsecond),  # 三级目录获取
    url(r'^user_getthird/$', views.user_getthird),  # 三级目录获取
    url(r'^db_list/$', views.db_list),  # db展示页面
    url(r'^page_Sql/$', views.page_Sql),  # 添加sql选项卡
    url(r'^sql_name/$', views.sql_name),  # 添加sql选项卡
    url(r'^sql_append', views.sql_append),  # 生成sql页面
    url(r'^sql_save/$', views.sql_save),  # sql保存页面
    url(r'^sql_update/$', views.sql_update), # 更新sql语句
    url(r'^delete_db/$', views.delete_db),  # 删除sql语句
    # url(r'^(.*)/(.*)/$', views.show_server),
    url(r'^service_type/$', views.service_type),  # 服务目录参数
    # url(r'^(.*)/(\w+)/$', views.data_uri),  # 服务目录跳转
    url(r'^welcome_dier/$',views.welcome_dier),  # 数据上架平台初始页面
    # 修改
    url(r'^update_acl/$', views.update_acl),  # 修改acl
    url(r'^update_control/$', views.update_control),  # 修改流量控制
    url(r'^update_user/$', views.update_username),  # 修改用户名
    url(r'^update_service', views.update_service),  # 修改服务
    # 四大通道路由
    url(r'^admin_file/$', views.admin_file),  # 文件通道路由
    url(r'^admin_ways/$', views.admin_ways),  # 消息通道名称
    url(r'^admin_interface/$', views.admin_interface),  # 接口通道名称
    url(r'^type_add/$', views.type_add),  # 添加四大通道数据到数据库
    url(r'^add_feild/$',views.add_field),  # 添加数据通道基础数据字段
    url(r'^journal/$', views.journal),

    url(r'^update_table/$', views.update_table),  # 数据源修改表名
    url(r'^update_field/$', views.update_field),  # 数据源修改字段
    url(r'^add_table/$', views.add_table),  # 管理员页面添加数据表操作
    url(r'^add_field/$', views.add_field),  # 管理员页面添加字段操作
    url(r'^field_show/$', views.field_show),  # 页面显示字段信息
    url(r'^table_delete/$', views.table_delete),  # 数据源删除数据表
    url(r'^field_delete/$', views.field_delete),  # 数据源删除字段操作
    url(r'^file_add/$', views.type_add),  # 添加三大通道类型
    url(r'^update_type/$', views.update_type),  # 修改三大通道类型
    url(r'^del_type/$', views.del_type),  # 删除三大通道
    url(r'sql_admin/$', views.sql_admin),  # select语句生成页面
    url(r'^update_data/$', views.update_data),  # sql写入文件
    url(r'^get_table/$', views.get_table),  # sql页面获取数据

    url(r'^get_datadier/$', views.get_datadier),  # 三级目录获取修改之前默认值
    url(r'^status_journal/$', views.status_journal),  # 状态日志页面
    url(r'^statistical_analysis/$', views.statistical_analysis),  # 统计分析页面

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
    url(r'^superAdmin/staAnaDatas/$', views.getTotalTop),  # 请求totalTop
    url(r'^update_sqls/$', views.update_Sql),  # 修改sql语句


    url(r'^desc/(.*)/$', views.desc_show),  # 查询所有表结构
    url(r'^loginEsgyn/$',views.serverLogin), # 易鲸捷登录
    url(r'loginOracle/$',views.oracleLogin), # oracle登录
    url(r'get_departs/$', views.get_departs), # 获取部门名称

    url(r'metadata_synchro/$', views.metadata_synchro),  # 元数据同步（表、字段结构）

    url(r'get_catalogInfo/$', views.get_cataloginfo), # 获取首页总览信息
    url(r'^jump_dpeartDetail/$', views.depart_classify),  # 点击侧边栏跳转到指定分类的部门信息中
    url(r'^user/(.*)/(\w+)/$', views.index),
    url(r'^get_departInfo/$',views.get_departInfo),
]
