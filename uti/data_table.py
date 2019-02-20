# -*- coding: utf-8 -*
from uti.db_connect import db_con


def table_show(data, request):
    # 获取session中的ip,端口,用户名,密码
    ip = request.session.get('ip')
    port = request.session.get('port')
    username = request.session.get('username')
    password = request.session.get('password')

    # 连接远程数据库
    sub_obj = db_con(ip, port, username, password)

    # 通过指定库名查询该数据库的所有表
    database = 'use %s; show tables;\n exit \n' % data
    database = database.encode(encoding='utf8')
    sub_obj.stdin.write(database)
    sub_obj.stdin.close()
    result_tables = sub_obj.stdout.read().decode().replace('\n', ',').split(',')

    # 过滤table中特殊字符
    table_list = []
    for table in result_tables:
        if table == '':
            pass
        else:
            table_list.append(table)
    sub_obj.stdout.close()

    # 过滤table不需要的字段
    for table in table_list:
        if table == 'Tables_in_'+data:
            table_list.remove(table)
    return table_list

