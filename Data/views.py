# -*- coding: utf-8 -*
"""
项目名称：数据上架系统
项目周期：2018年4月１6日－2018年5月14日
项目功能：主要实现了对任意远程数据库可以连接,查询到相应表的所有字段
        通过查询的字段形成sql的查询语句并形成对应部门的http字符串
        将sql语句和http字符串打包成参数通过对应接口传递到CSB平台
"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# from uti.data_table import table_show
# from superAdmin.models import UserGroup
# from py_mysql.lib import mysql
# from superAdmin.models import User
from uti.data_save import db_save
from uti.list_group import list_of_groups
import json
from uti.db_connect import db_con,con
from django.shortcuts import render
from Data.models import *
import logging
import requests
import xml.dom.minidom
from superAdmin.models import *
from threading import Thread
from time import sleep

logging = logging.getLogger('blog.views')


def server_list(request):
    """
    服务列表页显示
    :param request:
    :return:
    """
    username = request.session.get('username')
    # print(username, '#'*100)
    obj_first = User.objects.filter(username=username)
    for tiem in obj_first:
        first_id = tiem.first_id_id
        # print(first_id, 'f'*100)
        obj_dapartment = First.objects.filter(id=first_id)
        for tiem in obj_dapartment:
            dapartment = tiem.department
            # print(dapartment, 'D'*100)
        data_list = ServerDict.objects.filter(Q(server_name__icontains=dapartment, is_delete=0))
        paginator = Paginator(data_list, 4)
        page = request.GET.get("page")
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        return render(request, 'Data/server_list.html', {"page": contacts, 'paginator': paginator})


def test(request):
    aa = request.POST.get('page')
    print(aa,"*"*100)
    bb = int(aa)
    print(bb,"|")
    return render(request, 'Data/test.html')


def sql_server(request):
    """
    sql类型页面显示
    :param request:
    :return:
    """
    if request.method == 'POST':
        getSql = request.POST.get('get_sql')
        if getSql == '':
            return JsonResponse({"res": 0})
        else:
            request.session['getSql'] = getSql
            return JsonResponse({"res": 1})

    return render(request, "Data/sql_append.html")


def name_type(request):
    """
    添加名称类型页面显示
    :param request:
    :return:
    """
    if request.method == 'POST':
        serverName = request.POST.get('name')
        type = request.POST.get('type')
        if serverName == '':
            return JsonResponse({"res": 0})
        else:
            request.session['serverName'] = serverName
            request.session['type'] = type
            return JsonResponse({"res": 1})

    return render(request, 'Data/sql_name.html')


def data_base(request):
    """

    查询到所有数据库传给前端进行显示
    :param request:
    :return:
    """
    # 连接远程数据库
    sub_obj = db_con()
    # 查询mysql中的所有库
    sub_obj.stdin.write(b'show databases;\n exit \n')
    sub_obj.stdin.close()
    databases = sub_obj.stdout.read().decode().replace('\n', '.').split('.')
    # 将查询的所有库分割成一个库一个列表通过json传给前端
    dbs_list = []
    for i in databases:
        if i == '' or i == 'Database':
            pass
        else:
            dbs_list.append(i)
    list_dbs = list_of_groups(dbs_list, 1)
    return JsonResponse({'data': list_dbs})


# def desc_show(request, db_name, tb_name):
#     """
#     1.连接远程数据库
#     2.通过指定库名,表名查询相应的所有字段名称
#     3.将字段名称进行处理通过json传递给前端页面
#     :param request:
#     :param db_name:
#     :param tb_name:
#     :return:
#     """
#     # 连接远程数据库
#     sub_obj = db_con()
#     # 通过连接远程数据库查询库表的全部字段
#     desc_table = "select column_name from information_schema.COLUMNS " \
#                  "where table_name='%s'and" \
#                  " table_schema='%s';" % (tb_name, db_name)
#     desc_table = desc_table.encode(encoding='utf-8')
#     sub_obj.stdin.write(desc_table)
#     sub_obj.stdin.close()
#     result_desc = sub_obj.stdout.read().decode().replace('\n', ',').split(',')
#     # 将查询的表结构名称分成一个字段一个列表方便前端拼接字符串操作
#     desc_list = []
#     for i in result_desc:
#         if i == 'column_name' or i == '':
#             pass
#         else:
#             desc_list.append(i)
#     list_desc = list_of_groups(desc_list, 1)
#     return JsonResponse({'data': list_desc})

def desc_show(request, db_name):
    # db_name = []
    db_id = ''
    us_table = []
    field_info = []
    # us_china = getPinyin(china_db)
    # 连接点击的数据库
    china_db = request.session.get('user_login_name')
    db = con(china_db)
    cursor = db.cursor()
    sql = """select id,us_tableName from savetable where  tableName='{0}';""".format(db_name)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    dbs = cursor.fetchall()
    for db in dbs:
        db_id=db[0]
        us_table.append(db[1])
    # print(db_id,'#'*100)
    # print(dbs[0],"*"*100)
    sql = """select * from add_field where tableKey_id={0};""".format(db_id)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    field_list = cursor.fetchall()
    for field in field_list:
        field_info.append({'fieldName': field[1], 'fieldDesc': field[2],"us_table":us_table})
    # print(field_info, '*'*100)
    return JsonResponse({'data': field_info})


#def field_desc(request, db_name, tb_name, option_name):
#    """
#    1.通过库名,表名,字段名称来查询到相应字段名称的类型
#    2.将字段类型通过json传递给前端页面
#    :param request:
#    :param db_name:
#    :param tb_name:
#    :param option_name:
#    :return:
#    """
#    # 连接远程数据库
#    sub_obj = db_con()
#    # 通过连接远程数据库和对应字段名称获取该字段的字段类型
#    desc_table = "select COLUMN_TYPE from information_schema.COLUMNS " \
#                 "where  column_name='%s' " \
#                 "and table_name='%s'and" \
#                 " table_schema='%s';" % (option_name, tb_name, db_name)
#    desc_table = desc_table.encode(encoding='utf-8')
#    sub_obj.stdin.write(desc_table)
#    sub_obj.stdin.close()
#    result_desc = sub_obj.stdout.read().decode().replace('\n', ',').split(',')
#    # 将字段的类型通过json传给前端进行显示
#    table_field_desc_ = []
#    for i in result_desc:
#        if i == 'COLUMN_TYPE' or i == '':
#            pass
#        else:
#            table_field_desc_.append(i)
#    return JsonResponse({"res": table_field_desc_[0]})


def part_info(request):
    """
    获取到部门等信息传递到index页面
    :param request:
    :return:
    """
    # 通过session获取到部门等信息将部门信息传给index页面
    tp = request.session.get("tp")
    part = request.session.get('part')
    cata = request.session.get("cata")
    data = {"tp": tp, "part": part, "cata": cata}
    return HttpResponse(json.dumps(data), content_type="application/json")


def server_name(request):
    """
    服务名称页显示
    :param request:
    :return:
    """
    return render(request, 'Data/server_name.html')


def data_add(request):
    if request.method == 'POST':
        serverName = request.session.get('serverName')
        type = request.session.get('type')
        first = request.POST.get('first')
        second = request.POST.get('second')
        third = request.POST.get('third')
        topclass = '一级目录' + ':' + first + '<br>' + '二级目录' + ':' + second + '<br>' + '三级目录:' + third
        # print(catalog, '#'*100)
        result_first = First.objects.filter(chinese_abb=first)
        English_first = []
        English_second = []
        English_third = []
        for i in result_first:
            English_first.append(i.department)
        first_engilish = English_first[0]
        result_second = Second.objects.filter(chinese_abb=second)
        for i in result_second:
            English_second.append(i.industry)
        second_english = English_second[0]
        result_third = Third.objects.filter(chinese_abb=third)
        for i in result_third:
            English_third.append(i.species)
        third_english = English_third[0]

        if type == 'sql':
            getSql = request.session.get('getSql')
            result = db_save(serverName, topclass, type, first_engilish, second_english, third_english, data=getSql)
            if result:
                return JsonResponse({'res': 1})

        elif type == 'file':
            get_file = request.session.get('file_name')
            result = db_save(serverName, topclass, type, first_engilish, second_english, third_english, data=get_file)
            if result:
                return JsonResponse({'res': 1})

        elif type == 'interface':
            result = db_save(serverName, topclass, type, first_engilish, second_english, third_english, data='')
            if result:
                return JsonResponse({'res': 1})

    else:
        return JsonResponse({'res': 0})


def file_name(request):
    """
    session存储文件名称
    :param request:
    :return:
    """
    if request.method == 'POST':
        file_name_get = request.POST.get('file_name')
        if file_name_get == '':
            return JsonResponse({'res': 0})
        else:
            request.session['file_name'] = file_name_get
            return JsonResponse({'res': 1})


def del_server(request):

    if request.method == 'POST':
        serverdict_id = request.POST.get('check_id')
        ser_id = serverdict_id.split("_")
        for id in ser_id:
            if id == "":
                pass
            else:
                del_obj = ServerDict.objects.get(id=id)
                del_obj.is_delete = 1
                del_obj.save()
        # 0 :失败 1:成功
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res': 0})


def update_server_id(request):
    """
        修改功能函数
        :param request:
        :return:
        """
    if request.method == 'POST':
        updata_id = request.POST.get('updata_id')
        if updata_id == '':
            pass
        else:
            request.session['updata_id'] = updata_id
        # 0 :失败 1:成功
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res': 0})


def update_server_name(request):
    """
        修改功能函数
        :param request:
        :return:
        """
    if request.method == 'POST':
        name = request.POST.get('name')
        if name == '':
            pass
        else:
            updata_id = request.session.get('updata_id')
            print(updata_id, name)
            obj = ServerDict.objects.get(id=updata_id)
            obj.name = name
            obj.save()
            # 0 :失败 1:成功
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res': 0})


def file_server(request):
    """
    文件类型页面显示
    :param request:
    :return:
    """
    return render(request, 'Data/file_server.html')


def message_server(request):
    """
    信息类型页面显示
    :param request:
    :return:
    """
    return render(request, 'Data/message_server.html')


def interface_server(request):
    """
    服务类型页面显示
    :param request:
    :return:
    """
    return render(request, 'Data/interface_server.html')

# 三级联动目录


def page_Template(request):
    return render(request,'Data/page_Sql.html')


def select(request):

    return render(request, "Data/server_name.html")


def getFirst(request):
    username = request.session.get('username')
    # list1 = []
    # print(username, 'name'*100)
    obj_first_id = User.objects.filter(username=username)
    for item in obj_first_id:
        first_id = item.first_id_id
        # print(first_id, 'f'*100)
        first_name = First.objects.filter(id=first_id)
        for item in first_name:
            first_name = item.department
    oneList = First.objects.filter(is_delete=0, department=first_name)
    list2 = []
    for item in oneList:
        list2.append([item.id, item.chinese_abb])
        print(list2, '*'*30)
    return JsonResponse({'data': list2})


def getSecond(request, id):
    secondList = Second.objects.filter(first_id=id, is_delete=0)
    list1 = []
    for item in secondList:
        list1.append([item.id, item.first_id, item.chinese_abb])
    return JsonResponse({'data': list1})


def getThird(request, first_id,second_id):
    thirdList = Third.objects.filter(first_id =first_id,
                                     second_id=second_id,
                                     is_delete=0)
    list1 = []
    for item in thirdList:
        list1.append([item.id, item.chinese_abb])
    return JsonResponse({'data': list1})


def type_chose(request):
    """
    获取服务类型传给前端进行跳转页面
    :param request:
    :return:
    """
    type_server = request.session.get('type')
    return JsonResponse({'res': type_server})


def request_http(request):

    if request.method == 'POST':
        data_id = request.POST.get('data_id')
        print(data_id)
        data_id = data_id.split("_")
        list12 = []
        print(data_id)
        for id in data_id:
            if id == '':
                pass
            else:
                print(id)
                data_obj = ServerDict.objects.filter(id=id)
                obj = data_obj[0].data_name
                print(obj)
                data = {
                    "test": obj
                }
                dom = xml.dom.minidom.parse('./url_config/add_username.xml')
                root = dom.documentElement
                url = root.getElementsByTagName('url')[0].firstChild.data
                method = root.getElementsByTagName('requests')[0].firstChild.data
                # print(url,method)
                #
                # print(aa)
                res = requests.request(method=method, url=url, data=data)
                if res.status_code == 200:
                    print(11)


def interfaceTest(request):
    """
    接口测试页面
    :param request:
    :return:
    """
    return render(request, 'Data/interface_test.html')


# def add_username(request):
#
#     if request.method == 'POST':
#         dom = xml.dom.minidom.parse('./url_config/add_username.xml')
#         root = dom.documentElement
#         url = root.getElementsByTagName('url')[0].firstChild.data
#         method = root.getElementsByTagName('requests')[0].firstChild.data
#         print(url, method)
#         data = {"username": "zhangsan"}
#         res = requests.request(method=method,
#                                url=url,
#                                data=data
#                                )
#         if res.status_code == 200:
#             return JsonResponse({"result":res.text})
#
#
# def del_username(request):
#
#     if request.method == 'POST':
#         print(2)
#         dom = xml.dom.minidom.parse('./url_config/del_username.xml')
#         root = dom.documentElement
#         url = root.getElementsByTagName('url')[0].firstChild.data
#         method = root.getElementsByTagName('requests')[0].firstChild.data
#         data = {"userame": "zhangsan"}
#         print(url, method)
#         res = requests.request(method=method,
#                                url=url,
#                                data=data)
#         if res.status_code == 200:
#             print(res.text)
#
#             return JsonResponse({"result": res.text})
#
#
# def add_server(request):
#
#     if request.method == 'POST':
#         print(3)
#         dom = xml.dom.minidom.parse('./url_config/add_server.xml')
#         root = dom.documentElement
#         url = root.getElementsByTagName('url')[0].firstChild.data
#         method = root.getElementsByTagName('requests')[0].firstChild.data
#         print(url, method)
#         data = {"serviceName": "zhangsan",
#                 "hosts": "zs",
#                 "uris" : "/wjw/ggws/file/gxy/",
#                 "upstream_url":"http://192.168.2.130:8001/dafa/vatvad/davafar/vakbada"
#                 }
#         res = requests.request(method=method, url=url, data=data)
#
#         if res.status_code == 200:
#             print(res.text)
#             return JsonResponse({"result": res.text})
#
# def del_server1(request):
#
#     if request.method == 'POST':
#         print(4)
#         dom = xml.dom.minidom.parse('./url_config/del_server.xml')
#         root = dom.documentElement
#         url = root.getElementsByTagName('url')[0].firstChild.data
#         method = root.getElementsByTagName('requests')[0].firstChild.data
#         data = {"serviceName": "zhangsan"}
#         print(url, method)
#         res = requests.request(method=method,
#                                url=url,
#                                data=data)
#
#         if res.status_code == 200:
#             print(res.text)
#             return JsonResponse({"result": res.text})
#
#
# def add_group(request):
#     if request.method == 'POST':
#         print(5)
#         dom = xml.dom.minidom.parse('./url_config/add_group.xml')
#         root = dom.documentElement
#         url = root.getElementsByTagName('url')[0].firstChild.data
#         method = root.getElementsByTagName('requests')[0].firstChild.data
#         data = {"group": "zhangsan",
#                 "username":"zhangsan"}
#         print(url, method)
#         res = requests.request(method=method,
#                                url=url,
#                                data=data)
#         if res.status_code == 200:
#             print(res.text)
#             return JsonResponse({"result": res.text})
#
#
# def add_acl(request):
#
#     if request.method == 'POST':
#         print(6)
#         dom = xml.dom.minidom.parse('./url_config/add_acl.xml')
#         root = dom.documentElement
#         url = root.getElementsByTagName('url')[0].firstChild.data
#         method = root.getElementsByTagName('requests')[0].firstChild.data
#         data = {"serviceName": "云上平台",
#                 "name": "acl",
#                 "whitelist": "zhangsan"}
#         print(url, method)
#         res = requests.request(method=method,
#                                url=url,
#                                data=data)
#
#         if res.status_code == 200:
#             print(res.text)
#             return JsonResponse({"result": res.text})
#
#
# def del_acl(request):
#
#     if request.method == 'POST':
#         print(7)
#         dom = xml.dom.minidom.parse('./url_config/del_acl.xml')
#         root = dom.documentElement
#         url = root.getElementsByTagName('url')[0].firstChild.data
#         method = root.getElementsByTagName('requests')[0].firstChild.data
#         data = {"serviceName": "云上平台",
#                 "id": ""}
#         print(url, method)
#         res = requests.request(method=method, url=url, data=data)
#         if res.status_code == 200:
#             print(res.text)
#             return JsonResponse({"result": res.text})
#
#
# def add_control(request):
#
#     if request.method == 'POST':
#         print(7)
#         dom = xml.dom.minidom.parse('./url_config/add_control.xml')
#         root = dom.documentElement
#         url = root.getElementsByTagName('url')[0].firstChild.data
#         method = root.getElementsByTagName('requests')[0].firstChild.data
#         data = {"name": "rate-limiting",
#                 "consumer_id":"42e9115-545115-1513135-4848",
#                 "day": "2",
#                 "serviceName": "大数据法人库"}
#
#         print(url, method)
#         res = requests.request(method=method, url=url, data=data)
#         if res.status_code == 200:
#             print(res.text)
#             return JsonResponse({"result": res.text})
#
#
# def del_control(request):
#
#     if request.method == 'POST':
#         print(7)
#         dom = xml.dom.minidom.parse('./url_config/del_control.xml')
#         root = dom.documentElement
#         url = root.getElementsByTagName('url')[0].firstChild.data
#         method = root.getElementsByTagName('requests')[0].firstChild.data
#         data = {"id": "11531-156113-1513248-4531",
#                 "serviceName": "大数据法人库"}
#         print(url, method)
#         res = requests.request(method=method,
#                                url=url,
#                                data=data)
#
#         if res.status_code == 200:
#             print(res.text)
#             return JsonResponse({"result": res.text})

#　用户操作数据
# def integ_command(request):
#     """
#     接口总命令
#     :param : url_config
#     :return: response
#     """
#     # 添加用户
#     if request.method == "POST":
#
#         url_config = request.POST.get("req_config")
#         # print(url_config)
#         # print(url_config)
#         if url_config == "add_username":
#             username = request.POST.get("username")
#             # print(username)
#             xml_obj = xml.dom.minidom.parse('./url_config/add_username.xml')
#             # print(xml_obj)
#             root = xml_obj.documentElement
#             url = root.getElementsByTagName('url')[0].firstChild.data
#             method = root.getElementsByTagName('requests')[0].firstChild.data
#             params = {"username": username}
#             result = Uuser.objects.filter(username=username)
#             # result == 0 为 用户已存在 result == 1 用户不存在
#             # print(result)
#             if result:
#                 return JsonResponse({'result': 0})
#             else:
#                 obj = Uuser.objects.create(username=username)
#                 obj.save()
#
#                     # res = requests.request(method="GET", url="http://www.454")
#                 res = requests.request(method=method,
#                                        url=url,
#                                        data=params)
#
#                 # try:
#                 #     res = requests.request(method=method,
#                 #                            url=url,
#                 #                            data=params)
#                 # except:
#                 #     print(123)
#
#                 # finally:
#                 #     print(456)
#
#                 # finally:
#
#                 # res = requests.request(method="GET", url="http://www.baidu.com")
#                 # return JsonResponse({"result": 1})
#
#                 # res = requests.request(method="GET",url="http://www.baidu.com")
#                 # if res.status_code == 200:
#
#         # 删除用户
#         elif url_config == "del_username":
#             xml_obj = xml.dom.minidom.parse('./url_config/del_username.xml')
#             root = xml_obj.documentElement
#             url = root.getElementsByTagName('url')[0].firstChild.data
#             method = root.getElementsByTagName('requests')[0].firstChild.data
#             username = request.POST.get("username")
#             params = {"username": username}
#             print(url)
#             Uuser.objects.filter(username=username).delete()
#             result = Uuser.objects.filter(username=username)
#             # print(result)
#             if result:
#                 return JsonResponse({'result': 0})
#             else:
#                 # res = requests.request(method=method,
#                 #                        url=url,
#                 #                        data=params)
#                 return JsonResponse({"result": 1})
#                 # print(res.url)
#             # if res.status_code == 200:
#                 # print(res.text)
#         # 添加服务
#         elif url_config == "add_server":
#             xml_obj = xml.dom.minidom.parse('./url_config/add_server.xml')
#             root = xml_obj.documentElement
#             url = root.getElementsByTagName('url')[0].firstChild.data
#             method = root.getElementsByTagName('requests')[0].firstChild.data
#             serviceName = request.POST.get("serviceName")
#             hosts = request.POST.get("hosts")
#             uris = request.POST.get("uris")
#             upstream_url = request.POST.get("upstream_url")
#             print(xml_obj, url, method, serviceName, hosts, uris, upstream_url)
#             data = {"serviceName": serviceName,
#                     "hosts": hosts,
#                     "uris": uris,
#                     "upstream_url": upstream_url
#                     }
#             print(data)
#             result = Uservice.objects.filter(serviceName=serviceName)
#             if result:
#                 return JsonResponse({'result': 0})
#             else:
#                 obj = Uservice.objects.create(serviceName=serviceName,
#                                              hosts=hosts,
#                                              uris=uris,
#                                              upstream_url=upstream_url
#                                              )
#                 obj.save()
#                 # res = requests.request(method=method,
#                 #                        url=url,
#                 #                        data=data)
#                 return JsonResponse({"result": 1})
#             #  print(res.text)
#             # if res.status_code == 200:
#             # id = request.session['getSql'] =
#
#         # 删除服务
#         elif url_config == "del_server":
#             serviceName = request.POST.get("serviceName")
#             xml_obj = xml.dom.minidom.parse('./url_config/del_server.xml')
#             root = xml_obj.documentElement
#             url = root.getElementsByTagName('url')[0].firstChild.data
#             method = root.getElementsByTagName('requests')[0].firstChild.data
#             params = {"serviceName": serviceName}
#             print(serviceName, url, method, params)
#
#             Uservice.objects.filter(serviceName=serviceName).delete()
#             result = Uservice.objects.filter(serviceName=serviceName)
#             if result:
#                 return JsonResponse({'result': 0})
#             else:
#
#                 # res = requests.request(method=method,
#                 #                        url=url,
#                 #                        params=params)
#                 return JsonResponse({'result': 1})
#
#         # 添加组
#         elif url_config == "add_group":
#             xml_obj = xml.dom.minidom.parse('./url_config/add_group.xml')
#             root = xml_obj.documentElement
#             url = root.getElementsByTagName('url')[0].firstChild.data
#             method = root.getElementsByTagName('requests')[0].firstChild.data
#             group = request.POST.get("group")
#             username = request.POST.get("username")
#             params = {"group": group,
#                       "username": username
#                       }
#             result = Uuser.objects.filter(username=username)
#             if result:
#                 obj = Ugroup.objects.create(group=group,
#                                            username=username
#                                            )
#                 obj.save()
#                 # res = requests.request(method=method,
#                 #                        url=url,
#                 #                        data=params)
#                 return JsonResponse({"result": 1})
#             else:
#                 return JsonResponse({"result": 0})
#             # if res.status_code == 200:
#             #     print(res.text)
#
#         # 添加acl
#         elif url_config == "add_acl":
#             xml_obj = xml.dom.minidom.parse('./url_config/add_acl.xml')
#             root = xml_obj.documentElement
#             url = root.getElementsByTagName('url')[0].firstChild.data
#             method = root.getElementsByTagName('requests')[0].firstChild.data
#             serviceName = request.POST.get("serviceName")
#             name = request.POST.get("name")
#             whitelist = request.POST.get("whitelist")
#             params = {"serviceName": serviceName,
#                       "name": name,
#                       "whitelist": whitelist
#                       }
#             print(url, method, params)
#             result = Uservice.objects.filter(serviceName=serviceName)
#             if result:
#                 obj = Uacl.objects.create(serviceName=serviceName,
#                                          name=name,
#                                          whitelist=whitelist
#                                          )
#                 obj.save()
#                 # res = requests.request(method=method,
#                 #                        url=url,
#                 #                        data=params)
#                 return JsonResponse({"result": 1})
#             else:
#                 return JsonResponse({"result": 0})
#             # if res.status_code == 200:
#             # consumer_id = request.session['getSql'] = getSql
#
#         # 删除acl
#         elif url_config == "del_acl":
#             print(123)
#             serviceName = request.POST.get("serviceName")
#             print(serviceName)
#             xml_obj = xml.dom.minidom.parse('./url_config/del_acl.xml')
#             root = xml_obj.documentElement
#             url = root.getElementsByTagName('url')[0].firstChild.data
#             print(url)
#             method = root.getElementsByTagName('requests')[0].firstChild.data
#             # id = request.session.get("id")
#             # id = get_service_id(serviceName)
#             # params = {"serviceName": serviceName,
#             #           "id": id
#             #           }
#             Uacl.objects.filter(serviceName=serviceName).delete()
#             result = Uacl.objects.filter(serviceName=serviceName)
#             if result:
#                 return JsonResponse({"result": 0})
#             else:
#                 # res = requests.request(method=method,
#                 #                        url=url,
#                 #                        data=params)
#                 return JsonResponse({"result": 1})
#             # print(res.url)
#             # if res.status_code == 200:
#             #    print(res.text)
#
#
#         # 添加控制
#         elif url_config == "add_control":
#             xml_obj = xml.dom.minidom.parse('./url_config/add_control.xml')
#             print(xml_obj, url_config)
#             root = xml_obj.documentElement
#             url = root.getElementsByTagName('url')[0].firstChild.data
#             print(url)
#             method = root.getElementsByTagName('requests')[0].firstChild.data
#             print(method)
#             name = request.POST.get("name")
#             print(name)
#             day = request.POST.get("day")
#             print(day)
#             serviceName = request.POST.get("serviceName")
#             print(serviceName)
#             # consumer_id = request.session.get("consumer_id")
#             consumer_id= "11cd88d2-3e6a-464f-8dc3-5c1a42e8c54b"
#             params = {"name": name,
#                       "day": day,
#                       "serviceName": serviceName,
#                       "consumer_id": consumer_id
#                       }
#
#             print(params)
#             print(1)
#             obj = Ucontrols.objects.create(name=name,
#                                           day=day,
#                                           serviceName=serviceName,
#                                           consumer_id=consumer_id)
#             obj.save()
#             res = requests.request(method=method,
#                                    url=url,
#                                    data=params)
#             # if res.status_code == 200:
#             print(res)
#             return JsonResponse({"result": 1})
#
#
#         # 删除控制
#         elif url_config == "del_control":
#             xml_obj = xml.dom.minidom.parse('./url_config/del_control.xml')
#             root = xml_obj.documentElement
#             url = root.getElementsByTagName('url')[0].firstChild.data
#             method = root.getElementsByTagName('requests')[0].firstChild.data
#             serviceName = request.POST.get("serviceName")
#             id = get_service_id(serviceName)
#             print(url, method, serviceName)
#             params = {"id": id,
#                       "serviceName": serviceName}
#
#             obj = Ucontrols.objects.filter(serviceName=serviceName).delete()
#             res = requests.request(method=method, url=url, data=params)
#             print(params)
#             # if res.status_code == 200:
#             print(res)
#             return JsonResponse({"result": 1})


# 查询apikey
def get_apikey(request):

    xml_obj = xml.dom.minidom.parse('./url_config/req_apikey.xml')
    root = xml_obj.documentElement
    url = root.getElementsByTagName('url')[0].firstChild.data
    method = root.getElementsByTagName('requests')[0].firstChild.data
    username = request.POST.get("username")
    print(username)
    # params = {"username": username}
    # res = requests.request(method=method,
    #                        url=url,
    #                        data=params)
    # res_dict = json.loads(res.text)
    # result = res_dict.get("result")
    result = '测试'
    return JsonResponse({"result": username})


# 查询服务id
def get_service_id(serviceName):
    xml_obj = xml.dom.minidom.parse('./url_config/req_service_id.xml')
    root = xml_obj.documentElement
    url = root.getElementsByTagName('url')[0].firstChild.data
    method = root.getElementsByTagName('requests')[0].firstChild.data
    params = {'serviceName': serviceName}

    print(url,method,serviceName,'get'*100)
    res = requests.request(method=method, url=url, params=params)
    print(res.text,'res'*100)
    res_dict = json.loads(res.text)
    result = res_dict.get("result")
    result = result.get("result")
    return result


# 管理员操作数据
# def admin_command(request):
#     # 添加用户
#     if request.method == "POST":
#
#         url_config = request.POST.get("req_config")
#         if url_config == "add_username":
#             username = request.POST.get("username")
#             result = Auser.objects.filter(username=username)
#             # result == 0 为 用户已存在 result == 1 用户不存在
#             if result:
#                 return JsonResponse({'result': 0})
#             else:
#                 obj = Auser.objects.create(username=username)
#                 obj.save()
#                 return JsonResponse({'result': 0})
#
#         # 删除用户
#         elif url_config == "del_username":
#             username = request.POST.get("username")
#             Auser.objects.filter(username=username).delete()
#             result = Auser.objects.filter(username=username)
#             if result:
#                 return JsonResponse({'result': 0})
#             else:
#                 return JsonResponse({"result": 1})
#
#         # 添加服务
#         elif url_config == "add_server":
#             serviceName = request.POST.get("serviceName")
#             hosts = request.POST.get("hosts")
#             uris = request.POST.get("uris")
#             upstream_url = request.POST.get("upstream_url")
#             result = Aservice.objects.filter(serviceName=serviceName)
#             if result:
#                 return JsonResponse({'result': 0})
#             else:
#                 obj = Aservice.objects.create(serviceName=serviceName,
#                                               hosts=hosts,
#                                               uris=uris,
#                                               upstream_url=upstream_url
#                                               )
#                 obj.save()
#                 return JsonResponse({"result": 1})
#
#         # 删除服务
#         elif url_config == "del_server":
#             serviceName = request.POST.get("serviceName")
#             Aservice.objects.filter(serviceName=serviceName).delete()
#             result = Aservice.objects.filter(serviceName=serviceName)
#             if result:
#                 return JsonResponse({'result': 0})
#             else:
#                 return JsonResponse({'result': 1})
#
#         # 添加组
#         elif url_config == "add_group":
#             group = request.POST.get("group")
#             username = request.POST.get("username")
#             result = Auser.objects.filter(username=username)
#             if result:
#                 obj = Agroup.objects.create(group=group,
#                                             username=username
#                                             )
#                 obj.save()
#                 return JsonResponse({"result": 1})
#             else:
#                 return JsonResponse({"result": 0})
#
#         # 添加acl
#         elif url_config == "add_acl":
#             serviceName = request.POST.get("serviceName")
#             name = request.POST.get("name")
#             whitelist = request.POST.get("whitelist")
#             result = Aservice.objects.filter(serviceName=serviceName)
#             if result:
#                 obj = Aacl.objects.create(serviceName=serviceName,
#                                           name=name,
#                                           whitelist=whitelist
#                                           )
#                 obj.save()
#                 return JsonResponse({"result": 1})
#             else:
#                 return JsonResponse({"result": 0})
#
#         # 删除acl
#         elif url_config == "del_acl":
#             serviceName = request.POST.get("serviceName")
#             Aacl.objects.filter(serviceName=serviceName).delete()
#             result = Aacl.objects.filter(serviceName=serviceName)
#             if result:
#                 return JsonResponse({"result": 0})
#             else:
#                 return JsonResponse({"result": 1})
#
#         # 添加控制
#         elif url_config == "add_control":
#             name = request.POST.get("name")
#             day = request.POST.get("day")
#             serviceName = request.POST.get("serviceName")
#             consumer_id = "11cd88d2-3e6a-464f-8dc3-5c1a42e8c54b"
#             obj = Acontrols.objects.create(name=name,
#                                            day=day,
#                                            serviceName=serviceName,
#                                            consumer_id=consumer_id)
#             obj.save()
#             return JsonResponse({"result": 1})
#
#         # 删除控制
#         elif url_config == "del_control":
#             serviceName = request.POST.get("serviceName")
#             obj = Acontrols.objects.filter(serviceName=serviceName).delete()
#             result = Acontrols.objects.filter(serviceName=serviceName)
#             if result:
#                 return JsonResponse({'result': 0})
#             else:
#                 return JsonResponse({"result": 1})


if __name__ == '__main__':

    pass


