#coding:utf-8
from django.shortcuts import render
import subprocess
import xml
import math
import time
import pymysql
import requests
from django.shortcuts import render
from django.http import JsonResponse
from Data.views import get_service_id
#from superAdmin.models import User
# from superAdmin.models import UserGroup
# Create your views here.
# from superAdmin.models import User, ServerInfo, Users, Controls, Service, ACL
from superAdmin.models import *
from Data.models import First, ServerDict
from Data_app.models import *
from Safe_dic.models import *
from Service_app.models import *
from uti.db_connect import db_con
from uti.list_group import list_of_groups
from uti.db_connect import db_con,con,sub_sql
from uti.db_connect import send_log
from uti.usercode import getPinyin
import json
import re

# Create your views here.
# 获取用户的身份


def index(request, data,user_login_name):
    depart_list = []
    request.session['user_login_name'] = user_login_name
    print(user_login_name,'*'*100)

    depart = Department.objects.filter(us_dataname=user_login_name)
    for time in depart:
        departs = time.dataname
        print(departs, "*" * 100)
    depart_list.append(departs)

    db = con(user_login_name)
    cursor = db.cursor()
    sql = """select count(*) from Uservice"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    data_num = cursor.fetchall()[0][0]
    print(data_num)

    sql = """select count(*) from Uacl"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    acl_num = cursor.fetchall()[0][0]
    print(acl_num)

    sql = """select count(*) from Ucontrols"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    controls_num = cursor.fetchall()[0][0]
    print(controls_num)
    total_num = acl_num+controls_num
    all = total_num + data_num
    # print(a,'%'*100)
    db.close()

    return render(request, 'commonUser/index.html', {'user_login_name': user_login_name,
                                                     'depart_list': depart_list,
                                                     'data_num': data_num,
                                                     'acl_num': acl_num,
                                                     'controls_num': controls_num,
                                                     'total_num': total_num,
                                                     'all': all,
                                                     })


# 用户端显示acl
def acl_list(request):
    Uacl_list = []
    Aacl_list = []
    Uuser_list = []
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
    cursor = db.cursor()
    sql = 'select * from Uacl ;'
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    Uacls = cursor.fetchall()
    for uacl in Uacls:
        dict1 = {"serviceName": uacl[1], "name": uacl[2], "whitelist": uacl[3]}
        # print(dict1)
        Uacl_list.append(dict1)
    sql = 'select serviceName from Uservice ;'
    sql_ending = sql.encode(encoding="utf8")
    # print(sql)
    cursor.execute(sql_ending)
    serviceName = cursor.fetchall()
    for servicename in serviceName:
        dict1 = {"serviceName": servicename[0]}
        Aacl_list.append(dict1)
    db.commit()
    db.close()
    db = con('test')
    cursor = db.cursor()
    sql = """select username from Uuser where depart = '{0}';""".format(user_login_name)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    Uusers = cursor.fetchall()
    for Uuser in Uusers:
        print(Uuser[0])
        Uuser_list.append(Uuser[0])
    print(Uuser_list)
    db.commit()
    db.close()

    return render(request, 'commonUser/acl_list.html', {'Uacl': Uacl_list, 'Aacl': Aacl_list, 'Uuser': Uuser_list})


# 用户端显示流量访问控制
def control_list(request):
    Ucontrol_list = []
    user_list = []
    servicename_list = []
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
    # db = pymysql.connect('127.0.0.1', 'root', 'root', us_china, charset='utf8')
    cursor = db.cursor()
    sql = 'select * from Ucontrols ;'
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    Ucontrols = cursor.fetchall()
    for ucontrol in Ucontrols:
        dict1 = {"name": ucontrol[1], "username": ucontrol[2], "day": ucontrol[5], 'serviceName': ucontrol[4]}
        Ucontrol_list.append(dict1)
    db.commit()
    db.close()

    db = con('test')
    cursor = db.cursor()
    sql = """select username from Uuser where depart = '{0}';""".format(user_login_name)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    users = cursor.fetchall()
    for user in users:
            user_list.append({'username': user[0]})
    db.commit()
    db.close()

    db = con(user_login_name)
    cursor = db.cursor()
    sql = """select serviceName from Uservice;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    services = cursor.fetchall()
    for service in services:
        servicename_list.append({'servicename': service[0]})
    # # 提交到数据库执行
    db.commit()
    # # 关闭数据库连接
    db.close()

    return render(request, 'commonUser/control_list.html', {'Ucontrol': Ucontrol_list, 'username': user_list, 'servicename': servicename_list})


# 用户端显示服务目录
def service_list(request):

    page_list = []
    realm_list=""
    service_list = []
    # Aservice_list = []
    dbName_list = []
    fileName_list = []
    interfaceName_list = []
    messageName_list = []
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
    cursor = db.cursor()
    sql = 'select * from Uservice;'
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    services = cursor.fetchall()

    sql1 = 'select count(*) from Uservice;'
    sql1_ending = sql1.encode(encoding="utf8")
    cursor.execute(sql1_ending)
    count_data = cursor.fetchall()[0][0]
    pageCount= math.ceil(count_data/1)

    for service in services:

        print(service)
        dict1 = {"serviceName": service[1], "hosts": service[2], "uris": service[3], 'upstream_url': service[4]}
        # print(dict1)
        service_list.append(dict1)
    db.commit()
    db.close()
    db = con('test')
    cursor = db.cursor()
    sql = """select hosts from department where us_dataname='{0}';""".format(user_login_name)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_realm = cursor.fetchall()
    # realm_list = set_realm[0][0]
    for realm in set_realm:
        realm_list = realm[0]
    db.commit()
    db.close()
    db = con(user_login_name)
    cursor = db.cursor()

    sql = 'select dbName from dbList;'
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    dbNames = cursor.fetchall()
    for dbName in dbNames:
        dbName_list.append(dbName[0])
        # service_list.append({"dbName":dbName[0]})
        print(dbName_list)

    sql = """select fileName from fileList;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    fileNames = cursor.fetchall()
    for fileName in fileNames:
        fileName_list.append(fileName[0])

    sql = """select interfaceName from interfaceList;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    interfaceNames = cursor.fetchall()
    for interfaceName in interfaceNames:
        interfaceName_list.append(interfaceName[0])

    sql = """select messageName from messageList;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    messageNames = cursor.fetchall()
    for messageName in messageNames:
        messageName_list.append(messageName[0])

    # 提交到数据库执行
    db.commit()
    # 关闭数据库连接
    db.close()

    return render(request,
                  'commonUser/service_list.html',
                  {'Uservice': service_list,
                   'realm': realm_list,
                   'dbName_list': dbName_list,
                   'fileName_list': fileName_list,
                   'interfaceName_list': interfaceName_list,
                   'messageName_list': messageName_list,
                   'pageCount': pageCount,
                   })


# 用户操作页面
# 向数据库增加用户信息
def user_operation(request):
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    user_login_name = request.session.get('user_login_name')
    print(user_login_name,'user'*100)
    depname = request.POST.get('depname')
    print(depname,"++"*100)
    isTrue = True
    # 打开数据库连接
    # 判断数据库是否存在
    res = []
    uri = ''
    uris = ''
    task = ''
    name_obj = ''
    temp_val = ''
    interface_name = ''
    username = request.POST.get("username")

    if request.method == "POST":
        url_config = request.POST.get("req_config")
        print(url_config,'url_config'*100)
        # 增加用户
        if url_config == "add_username":
                db = con(user_login_name)
                cursor = db.cursor()
                # 去重
                sql = """select userName from Uuser where userName='{0}';""".format(username)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                user_name = cursor.fetchall()
                if user_name:
                    return JsonResponse({'result': 0})
                sql = """insert into Uuser values (null, "{0}");""".format(username)
                #   添加安全目录数据用户
                obj = User.objects.create(id=None,
                                          username=username,
                                          api_key='see',
                                          )

                obj.save(using='Safe_dic')
                xml_obj = xml.dom.minidom.parse('./url_config/add_username.xml')
                # print(xml_obj)
                root = xml_obj.documentElement
                url = root.getElementsByTagName('url')[0].firstChild.data
                method = root.getElementsByTagName('requests')[0].firstChild.data
                params = {"username": username}
                try:
                    res = requests.request(method=method,
                                           url=url,
                                           data=params,
                                           timeout=0.5)
                except requests.exceptions.ConnectionError:
                    isTrue = False
                except requests.exceptions.ReadTimeout:
                    isTrue = False

        # 删除用户
        elif url_config == "del_username":
            db = con(user_login_name)
            cursor = db.cursor()
            groupName_list = ''
            type_name = ''
            userName = request.POST.get("username")
            sql = """select groupName from Ugroup where userName = '{0}';""".format(userName)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            set_groupName = cursor.fetchall()
            for groupName in set_groupName:
                groupName_list = groupName[0]
            if groupName_list:
                sql = """delete from Ugroup where userName = '{0}'""".format(userName)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
            sql = """delete from Uuser where userName = "{0}";""".format(userName)
            # 删除安全目录用户
            obj = User.objects.filter(username=username)
            obj.delete()
            xml_obj = xml.dom.minidom.parse('./url_config/del_username.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            params = {"username": userName}
            try:
                res = requests.request(method=method,
                                       url=url,
                                       data=params,
                                       timeout=0.5)
            except requests.exceptions.ConnectionError:
                isTrue = False
            except requests.exceptions.ReadTimeout:
                isTrue = False

        # 增加服务目录
        elif url_config == "add_server":

            db = con('test')
            cursor = db.cursor()
            sql = """select hosts from department where dataname='{0}';""".format(depname)
            print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            hosts = cursor.fetchall()[0][0]
            print(hosts)
            db.close()
            db = con(user_login_name)
            cursor = db.cursor()
            upstream_urls = ''
            serviceName = request.POST.get("serviceName")
            uris = request.POST.get("uris")
            firstSel = request.POST.get('firstSel')
            secondSel = request.POST.get('secondSel')
            thirdSel = request.POST.get('thirdSel')
            type_name = request.POST.get('type_name')
            client_type = request.POST.get('client_type')
            upstream_url = request.POST.get("upstream_url")
            type = request.POST.get('type')
            name_obj = serviceName

            if type_name == 'db':
                sql = """select dbIP from dbList where dbName='{0}'""".format(type)
                print(sql)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                upstream_list = cursor.fetchall()
                for upstream_u in upstream_list:
                    upstream_urls = upstream_u[0]
                cursor.execute(sql_ending)
                set_sql = cursor.fetchall()
                # print(set_sql)
                # id = set_sql[0][0]
                # interface_name = type_name+'='+set_sql[0][0]
                uris = '/' + getPinyin(
                    firstSel) + '/' + getPinyin(secondSel) + '/' + type_name + '/' + getPinyin(
                    thirdSel) + '/' + upstream_url
                uri = '/' + getPinyin(firstSel) + '/' + getPinyin(
                    secondSel) + '/' + type_name + '/' + getPinyin(thirdSel) + '/'
                # temp_val = type_name+'='+str(set_sql[0][0])
                sql = """select serviceName from Uservice where serviceName='{0}';""".format(serviceName)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                service_name = cursor.fetchall()
                if service_name:
                    res.append({"host": hosts, "user_login_name": user_login_name, "result": 0, "uri": uri,
                                "temp_val": temp_val})
                    return JsonResponse({"result": res})
                sql = """insert into Uservice values (null, "{0}","{1}","{2}","{3}","{4}");""".format(serviceName,
                                                                                                hosts, uris, client_type,
                                                                                                type)
            else:
                print('file')
                if type_name == "file":
                    sql = """select fileIP from fileList where fileName='{0}';""".format(type)
                elif type_name == "interface":
                    sql = """select interfaceIP from interfaceList where interfaceName = '{0}';""".format(type)
                elif type_name == "message":
                    sql = """select messageIP from messageList where messageName = '{0}';""".format(type)

                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                upstream_list = cursor.fetchall()
                for upstream_u in upstream_list:
                    upstream_urls = upstream_u[0]
                uris = '/' + getPinyin(
                    firstSel) + '/' + getPinyin(secondSel) + '/' + type_name + '/' + getPinyin(
                    thirdSel) + '/' + upstream_url
                temp_val = type_name + '=' + type
                uri = '/' + getPinyin(firstSel) + '/' + getPinyin(
                    secondSel) + '/' + type_name + '/' + getPinyin(thirdSel) + '/'
                sql = """select serviceName from Uservice where serviceName='{0}';""".format(serviceName)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                service_name = cursor.fetchall()
                if service_name:
                    res.append({"host": hosts, "user_login_name": user_login_name, "result": 0, "uri": uri,
                                "temp_val": temp_val})
                    return JsonResponse({"result": res})
                sql = """insert into Uservice values (null, "{0}","{1}","{2}","{3}","{4}");""".format(serviceName,
                                                                                                hosts, uris,client_type,
                                                                                                type)
                # 添加数据目录数据
            obj = DataName.objects.create(id=None,
                                          data_name=serviceName,
                                          domain_name=hosts,
                                          first_name=getPinyin(firstSel),
                                          second_name=getPinyin(secondSel),
                                          third_name=getPinyin(thirdSel),
                                          interface_type=type_name,
                                          interface_name=type,
                                          is_delete=0,
                                          )

            obj.save(using='Data_app')
            # 将数据目录添加到总表中
            all_obj = Uservice.objects.create(id=None,
                                              serviceName=serviceName,
                                              hosts=hosts,
                                              uris=uris,
                                              client_type=client_type,
                                              upstream_url=type)
            all_obj.save()

            xml_obj = xml.dom.minidom.parse('./url_config/add_server.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            data = {"serviceName": serviceName,
                    "hosts": hosts,
                    "uris": uris,
                    "upstream_url": upstream_urls
                    }
            # print(data)
            try:
                res = requests.request(method=method,
                                       url=url,
                                       data=data,
                                       timeout=0.5)
                task = "增加服务"
            except requests.exceptions.ReadTimeout:
                isTrue = False
                task = "增加服务"
            except requests.exceptions.ConnectionError:
                isTrue = False
                task = "增加服务"

        # 删除服务
        elif url_config == "del_server":
            db = con(user_login_name)
            cursor = db.cursor()
            serviceName = request.POST.get("serviceName")
            aclName_list = ''
            sql = """select aclName from Uacl where serviceName = '{0}';""".format(serviceName)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            name_obj = serviceName
            set_aclName = cursor.fetchall()
            for aclName in set_aclName:
                aclName_list = aclName[0]
            if aclName_list:
                sql = """delete from Uacl where serviceName = '{0}'""".format(serviceName)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
            sql = """ delete from Uservice where serviceName = "{0}"; """.format(serviceName)
            # print(sql)
            # 删除数据目录数据
            obj = DataName.objects.filter(data_name=serviceName)
            obj.delete()

            # 删除总表数据目录
            all_obj = Uservice.objects.filter(serviceName=serviceName)
            all_obj.delete()

            xml_obj = xml.dom.minidom.parse('./url_config/del_server.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            params = {"serviceName": serviceName}
            try:
                res = requests.request(method=method,
                                       url=url,
                                       params=params,
                                       timeout=0.5)
                task = "删除服务"
            except requests.exceptions.ConnectionError:
                isTrue = False
                task = "删除服务"
            except requests.exceptions.ReadTimeout:
                isTrue = False
                task = "删除服务"

        # 添加组
        elif url_config == "add_group":
            db = con(user_login_name)
            cursor = db.cursor()
            group = request.POST.get("group")
            userName = request.POST.get("username")
            # 去重
            sql = """select groupName from Ugroup where groupName='{0}';""".format(group)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            group_name = cursor.fetchall()
            if group_name:
                return JsonResponse({'result': 0})
            sql = """insert into Ugroup values (null, "{0}","{1}");""".format(group, userName)
            xml_obj = xml.dom.minidom.parse('./url_config/add_group.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            params = {"group": userName,
                      "username": userName
                     }
            try:
                res = requests.request(method=method,
                                       url=url,
                                       data=params,
                                       timeout=0.5)
            except requests.exceptions.ConnectionError:
                isTrue = False
            except requests.exceptions.ReadTimeout:
                isTrue = False
        # 添加acl
        elif url_config == "add_acl":
            db = con(user_login_name)
            cursor = db.cursor()
            serviceName = request.POST.get("serviceName")
            # aclName = request.POST.get("name")
            aclName = 'acl'
            # print (aclName)
            print(serviceName)
            name_obj = serviceName
            whitelist = request.POST.get("whitelist")
            print(whitelist[0])
            print(whitelist, '*' * 100)
            sql = """select serviceName,whitelist from Uacl where serviceName='{0}' and whitelist='{1}';""".format(serviceName, whitelist)
            print(sql,'&'*100)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            uacl_list = cursor.fetchall()
            print(uacl_list,'%'*100)
            if uacl_list:
                return JsonResponse({'result': 0})
            else:
                sql = """insert into Uacl values (null, "{0}","{1}","{2}");""".format(serviceName, aclName,
                                                                                      whitelist)

                obj = AccessControl.objects.create(serviceName=serviceName,
                                                   acl=aclName,
                                                   WhiteName=whitelist,
                                                   )
                obj.save(using='Safe_dic')
                xml_obj = xml.dom.minidom.parse('./url_config/add_acl.xml')
                root = xml_obj.documentElement
                url = root.getElementsByTagName('url')[0].firstChild.data
                method = root.getElementsByTagName('requests')[0].firstChild.data
                params = {"serviceName": serviceName,
                          "name": aclName,
                          "whitelist": whitelist
                          }
                print(url, method, params, '*'*100)
                try:
                    res = requests.request(method=method,
                                           url=url,
                                           data=params,
                                           timeout=0.5)
                    task = "添加访问控制"
                except requests.exceptions.ConnectionError:
                    isTrue = False
                    task = "添加访问控制"
                except requests.exceptions.ReadTimeout:
                    isTrue = False
                    task = "添加访问控制"

        # 删除acl
        elif url_config == "del_acl":
            db = con(user_login_name)
            cursor = db.cursor()
            serviceName = request.POST.get("serviceName")
            # print(1,serviceName)
            name_obj = serviceName
            xml_obj = xml.dom.minidom.parse('./url_config/del_acl.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            #id = get_service_id(serviceName)
            params = {"serviceName": serviceName,
                      # "id": id
                      }
            sql = """delete from Uacl where serviceName = "{0}";""".format(serviceName)
            # 删除安全目录访问控制
            obj = AccessControl.objects.filter(serviceName=serviceName)
            obj.delete()
            # print(sql)
            try:
                res = requests.request(method=method,
                                       url=url,
                                       data=params,
                                       timeout=0.5)
                task = "删除访问控制"
            except requests.exceptions.ConnectionError:
                isTrue = False
                task = "删除访问控制"
            except requests.exceptions.ReadTimeout:
                isTrue = False
                task = "删除访问控制"

        # 添加控制
        elif url_config == "add_control":
            consumer_id = ''
            db = con(user_login_name)
            cursor = db.cursor()
            name = request.POST.get("name")
            day = request.POST.get("day")
            serviceName = request.POST.get("serviceName")
            name_obj = serviceName
            userName = request.POST.get('username')

            # with open("./sql_file/id.txt", "r") as f:
            #     con_id = f.readlines()
            #     for consu_id in con_id:
            #         cons_id = consu_id.split(' ')
            #         if cons_id[0] == userName:
            #             consumer_id = cons_id[1]
            # print(consumer_id)
            sql = """select serviceName,userName from Ucontrols where serviceName='{0}' and userName='{1}';""".format(serviceName, userName)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            ucontrols_list = cursor.fetchall()
            if ucontrols_list:
                return JsonResponse({'result': 0})
            else:

                sql = """insert into Ucontrols values (null, "{0}","{1}","{2}","{3}","{4}");""".format(name,
                                                                                                       userName,
                                                                                                       consumer_id,
                                                                                                       serviceName,
                                                                                                       day,
                                                                                                       )
                # 添加安全目录流量控制
                obj = FlowControl.objects.create(
                    name=name,
                    username=userName,
                    serviceName=serviceName,
                    user_day=day,
                )
                obj.save(using='Safe_dic')
                xml_obj = xml.dom.minidom.parse('./url_config/add_control.xml')
                root = xml_obj.documentElement
                url = root.getElementsByTagName('url')[0].firstChild.data
                method = root.getElementsByTagName('requests')[0].firstChild.data
                # consumer_id = request.session.get("consumer_id")
                # consumer_id = "11cd88d2-3e6a-464f-8dc3-5c1a42e8c54b"
                # print(name, day, serviceName, consumer_id)
                params = {"name": name,
                          "day": day,
                          "serviceName": serviceName,
                          "username": username,
                          }
                print(params)
                print(method, url)
                try:
                    res = requests.request(method=method,
                                           url=url,
                                           data=params,
                                           timeout=0.5)
                    print(res)
                    task = "添加流量控制"
                except requests.exceptions.ConnectionError:
                    isTrue = False
                    task = "添加流量控制"
                except requests.exceptions.ReadTimeout:
                    isTrue = False
                    task = "添加流量控制"

        # 删除控制
        elif url_config == "del_control":
            db = con(user_login_name)
            cursor = db.cursor()
            userName = request.POST.get('username')
            serviceName = request.POST.get("serviceName")
            name_obj = serviceName
            # 删除安全目录流量控制
            obj = FlowControl.objects.filter(username=userName, serviceName=serviceName)
            obj.delete()
            sql = """delete from Ucontrols where serviceName = "{0}";""".format(serviceName)
            xml_obj = xml.dom.minidom.parse('./url_config/del_control.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            #id = get_service_id(serviceName)
            params = {"username": userName,
                      "serviceName": serviceName}
            print(params)
            try:
                res = requests.request(method=method,
                                       url=url,
                                       data=params,
                                       )
                task = "删除流量控制"
                isTrue = False
            except:
                pass
                #except requests.exceptions.ConnectionError:
                #isTrue = False
                #task = "删除流量控制"
                #except requests.exceptions.ReadTimeout:
                #isTrue = False
                #task = "删除流量控制"

        if isTrue == False:
            sql_ending = sql.encode(encoding="utf8")
        # print(sql)
            try:
            # 执行sql语句
                cursor.execute(sql_ending)
            # 提交到数据库执行
                db.commit()
                endtime = time.time()
                timeArray = time.localtime(endtime)
                endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                db = con(user_login_name)
                cursor = db.cursor()
                sql = """insert into commonlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, name_obj ,
                                                                                                           depname,
                                                                                                           airTime, endtime,
                                                                                                           "成功")
                print(sql)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                db.commit()
                db.close()

                db = con("test")
                cursor = db.cursor()
                sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                                       name_obj,
                                                                                                       depname,
                                                                                                       airTime,
                                                                                                       endtime,
                                                                                                       "成功")
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                db.commit()
                db.close()

                sendlog = str((task,
                               name_obj,
                               depname,
                               airTime,
                               endtime,
                               '成功'))
                sendLog = send_log(sendlog)

                if url_config == 'add_server':
                    res.append({"host": hosts, "user_login_name": user_login_name, "result": 1, "uri": uri, "temp_val": temp_val})
                    return JsonResponse({"result": res})
                else:
                    return JsonResponse({"result": 1})
            except:
                # 如果发生错误则回滚
                db.rollback()
                return JsonResponse({"result": 0})


# 服务目录传参
def service_type(request):
    temp_val = request.POST.get('temp_val')
    request.session['temp_val'] = temp_val
    return JsonResponse({'res':1})


def update_service(request):
    res = []
    depname = request.POST.get('depname')
    user_login_name = request.session.get('user_login_name')
    firstSel = request.POST.get('firstSel')
    secondSel = request.POST.get('secondSel')
    thirdSel = request.POST.get('thirdSel')
    serviceName = request.POST.get('old_serviceName')
    service_Name = request.POST.get('serviceName')
    # hosts = user_login_name + '.gz'
    type= request.POST.get('type_content')
    type_name = request.POST.get('type')
    client_type = request.POST.get('client_type')
    upstream_url = request.POST.get('add_upstream_url')
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    # 连接点击的数据库
    db = con(user_login_name)
    cursor = db.cursor()
    # 删除流量控制
    sql = """ delete from Uservice where serviceName = "{0}"; """.format(serviceName)
    # print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    obj = DataName.objects.filter(data_name=serviceName)
    obj.delete()

    # 删除总表数据目录
    all_obj = Uservice.objects.filter(serviceName=serviceName)
    all_obj.delete()

    db.commit()
    db.close()

    db = con('test')
    cursor = db.cursor()
    sql = """select hosts from department where dataname='{0}';""".format(depname)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    hosts = cursor.fetchall()[0][0]
    print(hosts,)
    db.close()

    db = con(user_login_name)
    cursor = db.cursor()
    # 添加流量控制

    if type_name == 'db':
        sql = """select dbSql from dbList where dbName='{0}';""".format(type)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        set_sql = cursor.fetchall()
        interface_name = type_name + '=' + set_sql[0][0]
        uris = '/' + getPinyin(firstSel) + '/' + getPinyin(
            secondSel) + '/' + type_name + '/' + getPinyin(thirdSel) + '/' + upstream_url
        # uri = '/' + getPinyin(firstSel) + '/' + getPinyin(secondSel) + '/' + type_name + '/' + getPinyin(
        #     thirdSel) + '/' + 'xxx?' + type_name
        # temp_val = type_name + '=' + set_sql[0][0]
        # 去重
        sql = """select serviceName from Uservice where serviceName='{0}';""".format(service_Name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        ser_name = cursor.fetchall()
        print(ser_name)
        if ser_name:
            return JsonResponse({'result': 0})
        sql = """insert into Uservice values (null, "{0}","{1}","{2}","{3}","{4}");""".format(service_Name, hosts, uris, client_type, type)
    else:
        interface_name = type_name + '=' + type
        uris = '/' + getPinyin(firstSel) + '/' + getPinyin(
            secondSel) + '/' + type_name + '/' + getPinyin(thirdSel) + '/' + upstream_url
        # temp_val = type_name + '=' + type
        # uri = '/' + getPinyin(firstSel) + '/' + getPinyin(secondSel) + '/' + type_name + '/' + getPinyin(
        #     thirdSel) + '/' + 'xxx?' + type_name
        # # 去重
        # sql = """select serviceName from Uservice where serviceName='{0}';""".format(service_Name)
        # sql_ending = sql.encode(encoding="utf8")
        # cursor.execute(sql_ending)
        # service_name = cursor.fetchall()
        # if service_name:
        #     return JsonResponse({'result': 0})
        sql = """insert into Uservice values (null, "{0}","{1}","{2}","{3}","{4}");""".format(service_Name, hosts, uris,client_type, type)
    # 添加数据目录数据
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()
    obj = DataName.objects.create(id=None,
                                  data_name=service_Name,
                                  domain_name=user_login_name + '.gz',
                                  first_name=getPinyin(firstSel),
                                  second_name=getPinyin(secondSel),
                                  third_name=getPinyin(thirdSel),
                                  interface_type=type_name,
                                  interface_name=interface_name,
                                  is_delete=0,
                                  )

    obj.save(using='Data_app')
    # 总表添加数据目录
    all_obj = Uservice.objects.create(id=None,
                                      serviceName=service_Name,
                                      hosts=hosts,
                                      uris=uris,
                                      client_type=client_type,
                                      upstream_url=type)
    all_obj.save()

    task = "修改服务"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    db = con(user_login_name)
    cursor = db.cursor()
    sql = """insert into commonlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, service_Name,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, service_Name,
                                                                                           depname,
                                                                                           airTime, endtime,
                                                                                           "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   service_Name,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({'result': 1})


# 修改acl
def update_acl(request):
    depname = request.POST.get('depname')
    depname = request.POST.get('depname')
    sername = request.POST.get('sername')
    newSerName = request.POST.get('newSerName')
    newWL = request.POST.get('newWL')
    user_login_name = request.session.get('user_login_name')
    sendlog = ''
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con(user_login_name)
    cursor = db.cursor()
    # 删除acl
    sql = """delete from Uacl where serviceName='{0}';""".format(sername)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    obj = AccessControl.objects.filter(serviceName=sername)
    obj.delete()
    # 添加acl
    sql = """insert into Uacl values (null,'{0}','acl','{1}');""".format(newSerName,newWL)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()
    obj = AccessControl.objects.create(serviceName=newSerName,
                                       acl='acl',
                                       WhiteName=newWL,
                                       )
    obj.save(using='Safe_dic')

    task = "修改访问控制"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con(user_login_name)
    cursor = db.cursor()
    sql = """insert into commonlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, newSerName,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, newSerName,
                                                                                           depname,
                                                                                           airTime, endtime,
                                                                                           "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   newSerName,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({'result':1})


# 修改流量控制
def update_control(request):
    sendlog = ''
    depname = request.POST.get('depname')
    name = "rate-limiting"
    username = request.POST.get('username')
    serviceName = request.POST.get('old_serviceName')
    newSerName = request.POST.get('newusername')
    newvicName = request.POST.get('servicename')
    consumer_id = '11cd88d2-3e6a-464f-8dc3-5c1a42e8c54b'
    newday = request.POST.get('day')
    user_login_name = request.session.get('user_login_name')
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con(user_login_name)
    cursor = db.cursor()
    # 删除流量控制
    sql = """delete from Ucontrols where userName= '{0}' and serviceName = "{1}";""".format(username,serviceName)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    obj = FlowControl.objects.filter(username=username,serviceName=serviceName)
    obj.delete()
    # 添加流量控制
    sql = """insert into Ucontrols values (null, "{0}","{1}","{2}","{3}","{4}");""".format(name, newSerName, consumer_id,newvicName, newday)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()
    # 添加安全目录流量控制
    obj = FlowControl.objects.create(
        name=name,
        username=newSerName,
        serviceName=newvicName,
        user_day=newday,
    )
    obj.save(using='Safe_dic')

    task = "修改流量控制"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con(user_login_name)
    cursor = db.cursor()
    sql = """insert into commonlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, serviceName,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, serviceName,
                                                                                           depname,
                                                                                           airTime, endtime,
                                                                                           "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   serviceName,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({'result':1})


# 用户端显示acl
def selectcheckbox(request):
    Uacl_list = []
    Aacl_list = []
    Uuser_list = []
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
    # db = pymysql.connect('127.0.0.1', 'root', 'root', us_china, charset='utf8')
    cursor = db.cursor()
    sql = 'select * from Uacl ;'
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    Uacls = cursor.fetchall()
    for uacl in Uacls:
        dict1 = {"serviceName": uacl[1], "name": uacl[2], "whitelist": uacl[3]}
        # print(dict1)
        Uacl_list.append(dict1)
    sql = 'select serviceName from Uservice ;'
    sql_ending = sql.encode(encoding="utf8")
    # print(sql)
    cursor.execute(sql_ending)
    serviceName = cursor.fetchall()
    for servicename in serviceName:
        dict1 = {"serviceName": servicename[0]}
        # print(dict1)
        Aacl_list.append(dict1)

    sql = 'select userName from Uuser ;'
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    Uusers = cursor.fetchall()
    for Uuser in Uusers:
        print(Uuser[0])
        Uuser_list.append(Uuser[0])
    print(Uuser_list)
    db.commit()
    # 关闭数据库连接
    db.close()

    return render(request, 'commonUser/select-checkbox.html', {'Uacl': Uacl_list, 'Aacl': Aacl_list, 'Uuser': Uuser_list})


def user_getfirst(request):
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
    # print(china_db,'%'*100)
    first_list = []
    # print(china_db)
    # print(db)
    cursor = db.cursor()
    sql = """select chinese_abb from AdminFirst;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    first_tuple = cursor.fetchall()
    for f_tup in first_tuple:
        for first_name in f_tup:
            first_list.append(first_name)
    # print(first_list,'*'*100)
    db.commit()
    db.close()
    return JsonResponse({'result': first_list})


def user_getsecond(request):
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
    second_list = []
    first = request.POST.get("first")
    print(first, "%"*100)
    cursor = db.cursor()
    sql = """select id from AdminFirst WHERE chinese_abb='{0}';""".format(first)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_first_id = cursor.fetchall()
    first_id = set_first_id[0][0]
    sql = """select chinese_abb from AdminSecond WHERE first_id='{0}';""".format(first_id)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_second_name = cursor.fetchall()
    for second_name in set_second_name:
        for name in second_name:
            second_list.append(name)
    print(second_list)
    db.commit()
    db.close()
    return JsonResponse({'result': second_list})


def user_getthird(request):
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
    third_list = []
    # print(db)
    second = request.POST.get("second")
    cursor = db.cursor()
    sql = """select id from AdminSecond WHERE chinese_abb='{0}';""".format(second)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_second_id = cursor.fetchall()
    second_id = set_second_id[0][0]
    sql = """select chinese_abb from AdminThird WHERE second_id='{0}';""".format(second_id)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_third_name = cursor.fetchall()
    for third_name in set_third_name:
        for name in third_name:
            third_list.append(name)
    db.commit()
    db.close()
    return JsonResponse({'result': third_list})


# 获取数据目录修改之前的三级目录值
def get_chname(request):

    catalog_list = []
    depname = request.POST.get('depname')
    erji = request.POST.get('erji')
    sanji = request.POST.get('sanji')
    siji = request.POST.get('siji')
    en_name = getPinyin(depname)

    db = con(en_name)
    cursor = db.cursor()
    sql = """select chinese_abb from AdminFirst where department='{0}';""".format(erji)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_first_name = cursor.fetchall()
    catalog_list.append({'first_name': set_first_name[0][0]})

    sql = """select chinese_abb from AdminSecond where industry='{0}';""".format(sanji)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_second_name = cursor.fetchall()
    catalog_list.append({'second_name': set_second_name[0][0]})
    print(catalog_list)
    sql = """select chinese_abb from AdminThird where species='{0}';""".format(siji)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_third_name = cursor.fetchall()
    catalog_list.append({'third_name': set_third_name[0][0]})
    print(set_third_name, 'third')
    print(catalog_list)
    db.close()
    print(catalog_list, '*'*100)
    return JsonResponse({'result': catalog_list})


# 分页函数
def page_nation(request):
    # dep_pname, table_name, page, depart, each, search, table_keys

    # None
    # search
    # test
    # depname
    # mylog
    # table_name
    # 2
    # page
    # 10
    # each_num
    search = ""
    # result = []
    page_list = []
    en_name = ''
    depname = request.POST.get('database')  # --数据库
    table_name = request.POST.get('table_name')  # --数据表
    page = request.POST.get('page')  # -- 第几页
    depart = request.POST.get('depart')  # --部门
    each = request.POST.get('each_num')  # -- 每页显示几条
    search = request.POST.get('search') # --搜索标识
    table_keys = request.POST.get('table_keys')  # --搜索值
    # depname = dep_pname
    each_num = int(each)
    print(search,'search')
    print(depname,'depname')
    print(table_name,'table_name')
    print(page,'page')
    print(each_num,'each_num')
    print(type(each_num))
    print(table_keys,'table_keys')
    #进入本地库
    if depname == 'test':
        en_name = depname
        en_depart = getPinyin(depart)
    #进入部门库
    else:
        en_name = getPinyin(depname)
        en_depart = getPinyin(depname)
        print(en_name,'&'*100)
    isTrue = isinstance(page, str)

    print(isTrue)
    #判断是否二次请求
    if isTrue == True:
        intpage = int(page)
        print(intpage, type(intpage))
        db = con(en_name)
        cursor = db.cursor()
        if search:
            if table_name == 'Uuser':
                # print(en_name,'%'*1000)
                sql = """select count(*) from {0} where depart='{1}' and {2} like '%{3}%';""".format(table_name, en_depart,table_keys,search)
                print(sql)
            else:
                print("查询")
                sql = """select count(*) from {0} where {1} like '%{2}%';""".format(table_name,table_keys,search)
                print(sql)

            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            count_data = cursor.fetchall()[0][0]
            print(count_data, ")" * 100)
            pageCount = math.ceil(count_data / each_num)

            if pageCount == 0:
                pageCount += 1
            print(pageCount)
            if table_name == 'Uuser':
                sql = """select * from {0} where depart='{1}' and {2} like '%{3}%'limit {4},{5};""".format(table_name, en_depart,table_keys,
                                                                                          search,
                                                                                          (intpage - 1) * each_num,
                                                                                          each_num)
            else:
                sql = """select * from {0} where {1} like '%{2}%'limit {3},{4};""".format(table_name, table_keys,search,
                                                                                               (intpage - 1)*each_num,
                                                                                               each_num)
                print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            pages = cursor.fetchall()
            for page in pages:
                print(page)
                page_list.append(page)
            print(page_list, '$' * 100)
            return JsonResponse({'pageCount': pageCount, 'result': page_list, 'allDataNum': count_data})
        else:
            print("展示")
            #获取页码条数
            if table_name == 'Uuser':
                # print(en_name,'%'*1000)
                sql = """select count(*) from {0} where depart='{1}';""".format(table_name, en_depart)
                print(sql)
            else:
                sql = """select count(*) from {0};""".format(table_name)
            #print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            count_data = cursor.fetchall()[0][0]
            print(count_data,")" * 100)
            pageCount = math.ceil(count_data / each_num)


            if pageCount == 0:
                pageCount += 1
            print(pageCount)


            if table_name == 'mylog':
                sql = """select * from {0} order by superAirtime desc limit {1},{2};""".format(table_name, (intpage-1)*each_num, each_num)

            elif table_name == 'departlog':
                sql = """select * from {0} order by detartAirtime desc limit {1},{2};""".format(table_name, (intpage-1)*each_num, each_num)

            elif table_name == 'commonlog':
                sql = """select * from {0} order by detartAirtime desc limit {1},{2};""".format(table_name, (intpage-1)*each_num, each_num)

            elif table_name == 'stalog':
                sql = """select * from {0} order by staTime desc limit {1},{2};""".format(table_name, (intpage-1)*each_num, each_num)


            elif table_name == 'Uuser':
                # depart = request.POST.get('depart')
                depart = depart
                en_depname = getPinyin(depart)

                # print(en_depname, '*'*1000)
                sql = """select * from {0} where depart='{1}' limit {2},{3};""".format(table_name, en_depname, (intpage-1)*each_num, each_num)

            else:
                sql = """select * from {0} order by id desc limit {1},{2};""".format(table_name, (intpage-1)*each_num, each_num)

            print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            pages = cursor.fetchall()
            for page in pages:
                print(page)
                page_list.append(page)
            print(page_list,'$'*100)
            return JsonResponse({'pageCount': pageCount, 'result': page_list, 'allDataNum': count_data})


# 分页函数
def page_nation_vue(dep_name, table_name, page, depart, each, search, table_keys):
    #

    # None
    # search
    # test
    # depname
    # mylog
    # table_name
    # 2
    # page
    # 10
    # each_num
    # result = []
    page_list = []
    en_name = ''
    # depname = request.POST.get('database')  # --数据库
    # table_name = request.POST.get('table_name')  # --数据表
    # page = request.POST.get('page')  # -- 第几页
    # depart = request.POST.get('depart')  # --部门
    # each = request.POST.get('each_num')  # -- 每页显示几条
    # search = request.POST.get('search') # --搜索标识
    # table_keys = request.POST.get('table_keys')  # --搜索值
    depname = dep_name
    each_num = int(each)
    print(search,'search')
    print(depname,'depname')
    print(table_name,'table_name')
    print(page,'page')
    print(each_num,'each_num')
    print(type(each_num))
    print(table_keys,'table_keys')
    #进入本地库
    if depname == 'test':
        en_name = depname
        en_depart = getPinyin(depart)
    #进入部门库
    else:
        en_name = getPinyin(depname)
        en_depart = getPinyin(depname)
        print(en_name,'&'*100)
    isTrue = isinstance(page, str)

    print(isTrue)
    #判断是否二次请求
    if isTrue == True:
        intpage = int(page)
        print(intpage, type(intpage))
        db = con(en_name)
        cursor = db.cursor()
        if search:
            if table_name == 'Uuser':
                # print(en_name,'%'*1000)
                sql = """select count(*) from {0} where depart='{1}' and {2} like '%{3}%';""".format(table_name, en_depart,table_keys,search)
                print(sql)
            else:
                print("查询")
                sql = """select count(*) from {0} where {1} like '%{2}%';""".format(table_name,table_keys,search)
                print(sql)

            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            count_data = cursor.fetchall()[0][0]
            print(count_data, ")" * 100)
            pageCount = math.ceil(count_data / each_num)

            if pageCount == 0:
                pageCount += 1
            print(pageCount)
            if table_name == 'Uuser':
                sql = """select * from {0} where depart='{1}' and {2} like '%{3}%'limit {4},{5};""".format(table_name, en_depart,table_keys,
                                                                                          search,
                                                                                          (intpage - 1) * each_num,
                                                                                          each_num)
            else:
                sql = """select * from {0} where {1} like '%{2}%'limit {3},{4};""".format(table_name, table_keys,search,
                                                                                               (intpage - 1)*each_num,
                                                                                               each_num)
                print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            pages = cursor.fetchall()
            for page in pages:
                print(page)
                page_list.append(page)
            print(page_list, '$' * 100)
            return JsonResponse({'pageCount': pageCount, 'result': page_list, 'allDataNum': count_data})
        else:
            print("展示")
            #获取页码条数
            if table_name == 'Uuser':
                # print(en_name,'%'*1000)
                sql = """select count(*) from {0} where depart='{1}';""".format(table_name, en_depart)
                print(sql)
            else:
                sql = """select count(*) from {0};""".format(table_name)
            #print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            count_data = cursor.fetchall()[0][0]
            print(count_data,")" * 100)
            pageCount = math.ceil(count_data / each_num)


            if pageCount == 0:
                pageCount += 1
            print(pageCount)


            if table_name == 'mylog':
                sql = """select * from {0} order by superAirtime desc limit {1},{2};""".format(table_name, (intpage-1)*each_num, each_num)

            elif table_name == 'departlog':
                sql = """select * from {0} order by detartAirtime desc limit {1},{2};""".format(table_name, (intpage-1)*each_num, each_num)

            elif table_name == 'commonlog':
                sql = """select * from {0} order by detartAirtime desc limit {1},{2};""".format(table_name, (intpage-1)*each_num, each_num)

            elif table_name == 'stalog':
                sql = """select * from {0} order by staTime desc limit {1},{2};""".format(table_name, (intpage-1)*each_num, each_num)


            elif table_name == 'Uuser':
                # depart = request.POST.get('depart')
                depart = depart
                en_depname = getPinyin(depart)

                # print(en_depname, '*'*1000)
                sql = """select * from {0} where depart='{1}' limit {2},{3};""".format(table_name, en_depname, (intpage-1)*each_num, each_num)

            else:
                sql = """select * from {0} order by id desc limit {1},{2};""".format(table_name, (intpage-1)*each_num, each_num)

            print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            pages = cursor.fetchall()
            for page in pages:
                print(page)
                page_list.append(page)
            print(page_list,'$'*100)
            return JsonResponse({'pageCount': pageCount, 'result': page_list, 'allDataNum': count_data})



