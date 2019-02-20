#-*- coding: utf-8 -*
import subprocess
import xml
from django.http import HttpResponse
import time
import pymysql
from django.contrib.sites import requests
from django.shortcuts import render
from django.http import JsonResponse
from Data.views import get_service_id
# from superAdmin.models import UserGroup
# Create your views here.
# from superAdmin.models import User, ServerInfo, Users, Controls, Service, ACL
from superAdmin.models import *
from Data.models import First, ServerDict
from Data_app.models import *
from Safe_dic.models import *
from Safe_dic.models import User as user
from Service_app.models import *
from uti.db_connect import db_con
from uti.list_group import list_of_groups
from uti.db_connect import db_con,con,sub_sql
from uti.get_num import get_num
from uti.usercode import getPinyin
from uti.sql_log import insert_log
from uti.db_connect import send_log
from uti.db_connect import get_status
from uti.db_connect import middle_con
# from uti.db_connect import input_status
import requests
import logging
import json
import re
import datetime
import sys
import os
import requests.packages.urllib3.util.ssl_
# from selenium import webdriver


def login(request):

    return render(request, 'superAdmin/login.html')


# 管理员初始页面
def welcome(request):

    client_list = []
    ipServiceCount_list = []
    db = con('test')
    cursor = db.cursor()
    sql = """select *  from stalog order by staTime desc;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    clientResult = cursor.fetchall()

    for data in clientResult:
        dict = {"data": data[0], "num": data[1], "time":data[2], "action":data[3], "serviceName":data[4], "service":data[5], "username":data[6],"status":data[7],"dataSize":data[8],"client":data[9]}
        client_list.append(dict)
    print(client_list, '--客户端访问次数')
    db.close()

    db = con('test')
    cursor = db.cursor()
    sql = """SELECT s.staDataName,count(1) as listcount,s.staIP FROM stalog s group by staDataName,staIP having count(1)>=1;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    IpServer = cursor.fetchall()

    for data in IpServer:
        print(data)
        dict = {"data": data[0], "num": data[1], "ip": data[2]}
        print(dict)
        ipServiceCount_list.append(dict)
    print(ipServiceCount_list, '--ipServiceCount')
    db.close()

    return render(request, 'superAdmin/welcome.html', {'client_list': client_list, 'ipServiceCount_list': ipServiceCount_list })


# 数据上架平台初始页面
def welcome_dier(request):

    return render(request, 'superAdmin/welcome_dier.html')


# 获取用户的身份
def index(request, data,user_login_name):

    request.session['user_login_name'] = user_login_name

    return render(request, 'superAdmin/index.html', {'user_login_name': user_login_name})


# 用户端页面显示用户信息
def user_list(request):

    Uuser_list = []
    # Auser_list = []
    depart = request.session.get('depart')
    print(depart, '--部门')
    # 首字母简写
    # us_china = getPinyin(depart)
    db = con('test')
    # db = pymysql.connect('127.0.0.1', 'root', 'root', us_china, charset='utf8')
    cursor = db.cursor()
    sql = 'select * from Uuser ;'
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    users = cursor.fetchall()
    for user in users:
        Uuser_list.append({"user": user[1], "apiKey": user[2]})
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)
    logging.debug("刷新用户列表")

    return render(request, 'superAdmin/user_list.html', {'Uuser': Uuser_list})


# 用户端页面显示用户组
def group_list(request):

    Ugroup_list = []
    Agroup_list = []
    depart = request.session.get('depart')
    # 首字母简写
    us_china = getPinyin(depart)
    db = con(us_china)
    cursor = db.cursor()
    sql = 'select * from Ugroup ;'
    sql_ending = sql.encode(encoding="utf8")
    # print(sql)
    cursor.execute(sql_ending)
    Ugroups = cursor.fetchall()
    for ugroup in Ugroups:
        dict1 = {"group": ugroup[1], "username": ugroup[2]}
        Ugroup_list.append(dict1)

    sql = 'select userName from Uuser ;'
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_userName = cursor.fetchall()
    for userName in set_userName:
        # print(userName)
        dict1 = {"username": userName[0]}
        # print(dict1)

        Agroup_list.append(dict1)
    # 提交到数据库执行
    db.commit()
    # 关闭数据库连接
    db.close()

    return render(request, 'superAdmin/group_list.html', {'Ugroup': Ugroup_list, 'Agroup': Agroup_list})


# 用户端显示流量访问控制
def control_list(request):

    Ucontrol_list = []
    user_list = []
    servicename_list = []
    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con(us_china)
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
    sql = """select username from Uuser where depart = '{0}';""".format(us_china)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    users = cursor.fetchall()
    for user in users:
            user_list.append({'username': user[0]})
    db.commit()
    db.close()
    db = con(us_china)
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

    return render(request, 'superAdmin/control_list.html', {'Ucontrol': Ucontrol_list, 'username': user_list, 'servicename': servicename_list})


# 用户端显示服务目录
def service_list(request):

    realm_list = ""
    service_list = []
    # Aservice_list = []
    dbName_list = []
    fileName_list = []
    interfaceName_list = []
    messageName_list = []
    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con(us_china)
    cursor = db.cursor()
    sql = 'select * from Uservice ;'
    # print(sql)
    sql_ending = sql.encode(encoding="utf8")
    # print(sql)
    cursor.execute(sql_ending)
    services = cursor.fetchall()
    for service in services:
        print(service,'--数据目录')
        dict1 = {"serviceName": service[1], "hosts": service[2], "uris": service[3], 'upstream_url': service[4]}
        # print(dict1)
        service_list.append(dict1)
    # sql = 'select * from Aservice ;'
    # sql_ending = sql.encode(encoding="utf8")
    # # print(sql)
    # cursor.execute(sql_ending)
    # Aservices = cursor.fetchall()
    # for Aservice in Aservices:
    #     dict1 = {"serviceName": Aservice[1], "hosts": Aservice[2], "uris": Aservice[3], 'upstream_url': Aservice[4]}
    #     # print(dict1)
    #     Aservice_list.append(dict1)
    # 提交到数据库执行
    db.commit()
    # 关闭数据库连接
    db.close()

    db = con('test')
    cursor = db.cursor()
    sql = """select hosts from department where dataname='{0}';""".format(depart)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_realm = cursor.fetchall()
    # realm_list = set_realm[0][0]
    for realm in set_realm:
        realm_list = realm[0]
    db.commit()
    # 关闭数据库连接
    db.close()
    db = con(us_china)
    cursor = db.cursor()

    sql = 'select dbName from dbList;'
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    dbNames = cursor.fetchall()
    for dbName in dbNames:
        dbName_list.append(dbName[0])
        # service_list.append({"dbName":dbName[0]})
        print(dbName_list,'--数据桥接名称')

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
                'superAdmin/service_list.html',
                 {'Uservice': service_list,
                  'realm': realm_list,
                  'dbName_list': dbName_list,
                  'fileName_list': fileName_list,
                  'interfaceName_list': interfaceName_list,
                  'messageName_list': messageName_list,
                  })


# 用户端显示acl
def acl_list(request):

    Uacl_list = []
    Aacl_list = []
    Uuser_list = []
    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con(us_china)
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
    db.commit()
    db.close()
    db = con('test')
    cursor = db.cursor()
    sql = """select username from Uuser where depart = '{0}';""".format(us_china)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    Uusers = cursor.fetchall()
    for Uuser in Uusers:
        Uuser_list.append(Uuser[0])
    print(Uuser_list, '--用户列表')
    db.commit()
    db.close()

    return render(request, 'superAdmin/acl_list.html', {'Uacl': Uacl_list, 'Aacl': Aacl_list, 'Uuser': Uuser_list})


def login_check(request):

    username = request.POST.get('username')
    # print(username, '*'*100)
    obj_set = User.objects.filter(username=username)
    for item in obj_set:
        # print(item.username, '1'*100)
        if item.username == username:
            request.session['username'] = username

            return JsonResponse({'res': 0})
        else:

            return JsonResponse({'res': 1})


#def user_manger(request):
#    user_list=[]
#    user_info = User.objects.all()
#    for obj in user_info:
#        first_id = obj.first_id_id
#        part_info = First.objects.filter(id=first_id)
#        for i in part_info:
#            part_name = i.chinese_abb
#            dict1 = {'username': obj.username, 'part_name': part_name, 'user_id': obj.user_id, 'api_key': obj.api_key}
#            user_list.append(dict1)
#    return render(request, 'superAdmin/user_manger.html',{"user_list":user_list})
#
#
#def auth_manger(request):
#    user_list = []
#    user_info = User.objects.all()
#    for obj in user_info:
#        first_id = obj.first_id_id
#        part_info = First.objects.filter(id=first_id)
#        for i in part_info:
#            part_name = i.chinese_abb
#            dict1 = {'username': obj.username, 'part_name': part_name, 'user_id': obj.user_id, 'api_key': obj.api_key}
#            user_list.append(dict1)
#    return render(request, 'superAdmin/auth_manger.html', {'user_info': user_list})
#
#
#def server_info(request):
#    data_list = []
#    userName = request.POST.get('name')
#    # print(username)
#    first_info = User.objects.filter(userName=userName)
#    for obj in first_info:
#        first_id = obj.first_id_id
#        first_name = First.objects.filter(id=first_id)
#        for i in first_name:
#            eng_name = i.department
#            data_info = ServerDict.objects.filter(server_name__contains=eng_name, is_delete=0)
#            for j in data_info:
#                data_catalog = j.data_name
#                # print(data_catalog)
#                data_list.append(data_catalog)
#    dict2 = {'server_name': data_list}
#    # for key,value in dict2.items():
#    #     print(value)
#    return JsonResponse({'res': dict2})
#
#
#def server_safe(request):
#    list1 = []
#    userName = request.POST.get('username')
#    info = request.POST.get('info')
#    info = info.split('_')
#    # print(username)
#    User_info = User.objects.filter(userName=userName)
#    for obj in User_info:
#        User_Id = obj.id
#        list1.append(User_Id)
#    # print(list1)
#    for i in info:
#        # print(i)
#        if i == '':
#            pass
#        else:
#            i = i.strip()
#            data_save = ServerInfo.objects.create(
#                id=None,
#                DataName=i,
#                UserId_id=list1[0]
#            )
#            data_save.save()
#    return JsonResponse({'res': 1})
#
#
#def only_look(request):
#    list2 = []
#    user_name = request.POST.get('user_name')
#    users = User.objects.filter(userName=user_name)
#    for obj in users:
#        user_id = obj.id
#        servers = ServerInfo.objects.filter(UserId_id=user_id)
#        for i in servers:
#            server_catalog = i.DataName
#            list2.append(server_catalog)
#    # print(list2)
#    dict3 = {'server_catalog': list2}
#
#    return JsonResponse({'res': dict3})


# 管理员操作页面
# 部门及数据表可视化

# 获取前端数据库
def admin_db(request):

    depart = request.POST.get('depart')
    request.session['depart'] = depart

    return JsonResponse({'result': 1})


# 目录栏显示初始页面
def admin(request):

    departTable = request.session.get('departTable')
    depart_list = []
    table_list = []
    table_china_list = []
    department_list = []
    depart_url = ''
    db = con('test')
    cursor = db.cursor()
    sql = """select name from dm_group;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    departments = cursor.fetchall()
    for department in departments:
        department_list.append(department[0])
    # print(department_list,'&'*100)
    depart = Department.objects.all()
    print(depart,'--部门')
    results = ''
    for time in depart:
        departs = time.dataname
        us_china = getPinyin(departs)
        depart_list.append(get_num(us_china))
        # print(depart_list)
        db = con(us_china)
        cursor = db.cursor()
        cursor.execute("show tables;")
        results = cursor.fetchall()
    db.close()
    # db = con('test')
    # cursor = db.cursor()
    # sql = """select count(*) from department """
    # sql_ending = sql.encode(encoding="utf8")
    # cursor.execute(sql_ending)
    # depart_num = cursor.fetchall()[0][0]
    # print(depart_num)
    # db.close()

    return render(request, 'superAdmin/back_admin.html', {'depart': depart_list,
                                                          'table': table_china_list,
                                                          'depart_url': depart_url,
                                                          'department_list': department_list    
                                                          })


# 管理员用户页面显示
# def admin_user(request):
#     Auser_list = []
#     depart = request.session.get('depart')
#     us_china = getPinyin(depart)
#     db = con(us_china)
#     # db = pymysql.connect('127.0.0.1', 'root', 'root', us_china, charset='utf8')
#     cursor = db.cursor()
#     sql = 'select * from Auser ;'
#     sql_ending = sql.encode(encoding="utf8")
#     # print(sql)
#     cursor.execute(sql_ending)
#     Asers = cursor.fetchall()
#     for Auser in Asers:
#         Auser_list.append(Auser[1])
#     # 提交到数据库执行
#     db.commit()
#     # 关闭数据库连接
#     db.close()

    # return render(request, 'superAdmin/admin_user.html', {'Auser': Auser_list})


# 管理员端显示用户组
# def admin_group(request):
#     Agroup_list = []
#     user_login_name = request.session.get('user_login_name')
#     # 首字母简写
#     # us_china = getPinyin(user_login_name)
#     db = con(user_login_name)
#     # db = pymysql.connect('127.0.0.1', 'root', 'root', us_china, charset='utf8')
#     cursor = db.cursor()
#     sql = 'select * from Agroup ;'
#     sql_ending = sql.encode(encoding="utf8")
#     # print(sql)
#     cursor.execute(sql_ending)
#     Agroups = cursor.fetchall()
#     for Agroup in Agroups:
#         dict1 = {"group": Agroup[1], "username": Agroup[2]}
#         # print(dict1)
#         Agroup_list.append(dict1)
#     # 提交到数据库执行
#     db.commit()
#     # 关闭数据库连接
#     db.close()
#
#     return render(request, 'superAdmin/admin_group.html', {'Agroup': Agroup_list})


# 管理员端显示流量控制
# def admin_control(request):
#     Acontrol_list = []
#     user_login_name = request.session.get('user_login_name')
#     # 首字母简写
#     # us_china = getPinyin(user_login_name)
#     db = con(user_login_name)
#     # db = pymysql.connect('127.0.0.1', 'root', 'root', us_china, charset='utf8')
#     cursor = db.cursor()
#     sql = 'select * from Acontrols ;'
#     sql_ending = sql.encode(encoding="utf8")
#     # print(sql)
#     cursor.execute(sql_ending)
#     Acontrols = cursor.fetchall()
#     for Acontrol in Acontrols:
#         dict1 = {"name": Acontrol[1], "consumer_id": Acontrol[2], "day": Acontrol[3], 'serviceName': Acontrol[4]}
#         # print(dict1)
#         Acontrol_list.append(dict1)
#     # 提交到数据库执行
#     db.commit()
#     # 关闭数据库连接
#     db.close()
#
#     return render(request, 'superAdmin/admin_control.html', {'control': Acontrol_list})


# 管理员端显示服务目录
# def admin_service(request):
#     Aservice_list = []
#     user_login_name = request.session.get('user_login_name')
#     # 首字母简写
#     # us_china = getPinyin(user_login_name)
#     db = con(user_login_name)
#     # db = pymysql.connect('127.0.0.1', 'root', 'root', us_china, charset='utf8')
#     cursor = db.cursor()
#     sql = 'select * from Aservice ;'
#     sql_ending = sql.encode(encoding="utf8")
#     # print(sql)
#     cursor.execute(sql_ending)
#     Aservices = cursor.fetchall()
#     for Aservice in Aservices:
#         dict1={"serviceName": Aservice[1], "hosts": Aservice[2], "uris": Aservice[3], 'upstream_url': Aservice[4]}
#         # print(dict1)
#         Aservice_list.append(dict1)
#     # 提交到数据库执行
#     db.commit()
#     # 关闭数据库连接
#     db.close()
#     return render(request, 'superAdmin/admin_service.html', {'Aservice': Aservice_list})


# 管理员端显示acl
# def admin_acl(request):
#     Aacl_list = []
#     user_login_name = request.session.get('user_login_name')
#     # 首字母简写
#     # us_china = getPinyin(user_login_name)
#     db = con(user_login_name)
#     # db = pymysql.connect('127.0.0.1', 'root', 'root', us_china, charset='utf8')
#     cursor = db.cursor()
#     sql = 'select * from Aacl ;'
#     sql_ending = sql.encode(encoding="utf8")
#     # print(sql)
#     cursor.execute(sql_ending)
#     Aacls = cursor.fetchall()
#     for Aacl in Aacls:
#         dict1={"serviceName": Aacl[1], "name": Aacl[2], "whitelist": Aacl[3]}
#         # print(dict1)
#         Aacl_list.append(dict1)
#     # 提交到数据库执行
#     db.commit()
#     # 关闭数据库连接
#     db.close()
#
#     return render(request, 'superAdmin/admin_acl.html', {'Aacl': Aacl_list})


# 三级目录显示页面
def admin_catalog(request):

    firstName_list = []
    # 获取点击的库名并转换成英文
    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con(us_china)
    # print(db)
    cursor = db.cursor()
    # 获取一级目录列表
    sql = 'select chinese_abb from AdminFirst;'
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    firstName_tuple = cursor.fetchall()
    for f_tuple in firstName_tuple:
        for firstName in f_tuple:
            map_path = getPinyin(firstName)
            firstName_list.append({"firstName": firstName, 'map_path': map_path})

    return render(request, 'superAdmin/admin_catalog.html', {'firstName_list': firstName_list})


# 获取二级目录信息
def second_list(request):

    first_list = []
    secondName_list = []
    # 获取选中的一级目录名称
    first_name = request.POST.get('first_name')
    # 获取点击的库名并转换成英文
    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con(us_china)
    # print(db)
    cursor = db.cursor()
    # 查询一级目录ｉｄ
    sql = """select id from AdminFirst where chinese_abb='{0}';""".format(first_name)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    first_tuple = cursor.fetchall()
    for F_tuple in first_tuple:
        for first_id in F_tuple:
            first_list.append(first_id)
    # 获取二级目录列表
    sql = """select chinese_abb from AdminSecond where first_id={0};""".format(first_list[0])
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    secondName_tuple = cursor.fetchall()
    for s_tuple in secondName_tuple:
        for secondName in s_tuple:
            us_secondName = getPinyin(secondName)
            secondName_list.append({'secondName': secondName, 'us_secondName': us_secondName})

    return JsonResponse({'data': secondName_list})


# 获取三级目录信息
def third_list(request):

    secondList = []
    secondName_list = []
    # 获取选中的二级目录
    second_name = request.POST.get('second_name')
    # 获取点击的库名并转换成英文
    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con(us_china)
    # print(db)
    cursor = db.cursor()
    # 获取二级目录id
    sql = """select id from AdminSecond where chinese_abb='{0}';""".format(second_name)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    second_tuple = cursor.fetchall()
    for S_tuple in second_tuple:
        for second_id in S_tuple:
            # print(second_id)
            secondList.append(second_id)
    sql = """select chinese_abb from AdminThird where second_id={0};""".format(secondList[0])
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    secondName_tuple = cursor.fetchall()
    for t_tuple in secondName_tuple:
        for thirdName in t_tuple:
            us_thirdName = getPinyin(thirdName)
            secondName_list.append({'thirdName': thirdName, 'us_thirdName': us_thirdName})

    return JsonResponse({'data': secondName_list})


# 获取一级目录内容
def catalog_info(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    result = []
    sendlog = ''
    # 获取一级目录名称
    first_info = request.POST.get('first_name')
    # print(first_info)
    en_first = getPinyin(first_info)
    # 获取点击的库名并转换成中文
    depart = request.session.get('depart')
    depname = depart
    us_china = getPinyin(depart)
    db = con(us_china)
    # print(db)
    cursor = db.cursor()
    sql = """select chinese_abb from AdminFirst where chinese_abb='{0}';""".format(first_info)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    select_name = cursor.fetchall()
    if select_name:
        result.append({'result': 0, 's': 0})
        return JsonResponse({'result': result})
    sql = """insert into AdminFirst values (null,"{0}","{1}",0);""".format(
             en_first, first_info)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()
    task = "添加一级目录"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, first_info, depname, airTime, endtime, "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                  first_info,
                  depname,
                  airTime,
                  endtime,
                  '成功'))
    sendLog = send_log(sendlog)
    map_path = getPinyin(first_info)
    result.append({'result': 1, 'map_path': map_path})

    return JsonResponse({'result': result})


def second_info(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    first_list = []
    result = []
    sendlog = ''
    firstInfo = request.POST.get('first_name')
    secondInfo = request.POST.get('second_name')
    # 获取英文简称
    en_second = getPinyin(secondInfo)
    # 获取点击的库名并转换成英文
    depart = request.session.get('depart')
    depname = depart
    us_china = getPinyin(depart)
    db = con(us_china)
    # print(db)
    cursor = db.cursor()
    sql = """select id from AdminFirst where chinese_abb='{0}';""".format(firstInfo)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    first_tuple = cursor.fetchall()
    for F_tuple in first_tuple:
        for first_id in F_tuple:
            first_list.append(first_id)
    sql = """select chinese_abb from AdminSecond where chinese_abb='{0}' and first_id={1};""".format(secondInfo, first_list[0])
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    select_name = cursor.fetchall()
    print(select_name)
    if select_name:
        result.append({'result': 0, 's': 0})
        return JsonResponse({'result': result})
    sql = """insert into AdminSecond values(null, '{0}', '{1}', 0, {2});""".format(en_second, secondInfo, first_list[0])
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    task = "添加二级目录"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                           secondInfo,
                                                                                           depname,
                                                                                           airTime,
                                                                                           endtime,
                                                                                           "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   secondInfo,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)
    map_path = getPinyin(secondInfo)
    result.append({'result': 1, 'map_path': map_path})

    return JsonResponse({'result': result})


def third_info(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    firstList = []
    secondList = []
    result = []
    sendlog = ''
    firstInfo = request.POST.get('first_name')
    secondInfo = request.POST.get('second_name')
    thirdInfo = request.POST.get('third_name')
    # print(firstInfo, secondInfo, thirdInfo)
    # 将三级目录转化成英文简称
    en_third = getPinyin(thirdInfo)
    # 获取点击的库名并转换成英文
    depart = request.session.get('depart')
    depname = depart
    us_china = getPinyin(depart)
    db = con(us_china)
    cursor = db.cursor()
    # 获取一级目录id
    sql = """select id from AdminFirst where chinese_abb='{0}';""".format(firstInfo)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    first_tuple = cursor.fetchall()
    for F_tuple in first_tuple:
        for first_id in F_tuple:
            firstList.append(first_id)
    # 获取二级目录id
    sql = """select id from AdminSecond where chinese_abb='{0}';""".format(secondInfo)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    second_tuple = cursor.fetchall()
    for S_tuple in second_tuple:
        for second_id in S_tuple:
            secondList.append(second_id)
    sql = """select chinese_abb from AdminThird where chinese_abb='{0}'  and second_id={1};""".format(thirdInfo, secondList[0])
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    select_name = cursor.fetchall()
    if select_name:
        result.append({'result': 0,'s':0})
        return JsonResponse({'result': result})
    sql = """insert into AdminThird values(null, '{0}', '{1}', 0, {2}, {3});""".format(en_third, thirdInfo, firstList[0], secondList[0])
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    # 添加服务目录数据
    obj = ServiceData.objects.create(id=None,
                                     link_name=us_china+'.gz',
                                     firstName=firstInfo,
                                     secondName=secondInfo,
                                     thirdName=thirdInfo,
                                     is_delete=0,
                                     )

    obj.save(using='Service_app')

    task = "添加三级目录"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                           thirdInfo,
                                                                                           depname,
                                                                                           airTime,
                                                                                           endtime,
                                                                                           "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   thirdInfo,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    map_path = getPinyin(thirdInfo)
    result.append({'result': 1, 'map_path': map_path})

    return JsonResponse({'result': result})


# 三级目录删除操作
def delete_catalog(request):
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    catalog_name = request.POST.get('delete_name')
    table_name = request.POST.get('dier')
    depart = request.session.get('depart')
    depname = depart
    sendlog = ''
    us_china = getPinyin(depart)
    if table_name == '一级目录':
        # 获取点击的库名并转换成英文
        db = con(us_china)
        # print(db)
        cursor = db.cursor()

        sql = """select id from AdminFirst where chinese_abb='{0}'""".format(catalog_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        sql_id = cursor.fetchall()
        for ids in sql_id:
            id = ids[0]

        sql = """delete from AdminThird where first_id = {0};""".format(id)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)

        sql = """delete from AdminSecond where first_id = {0};""".format(id)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)

        sql = """delete from AdminFirst where chinese_abb='{0}'""".format(catalog_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "删除一级目录"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               catalog_name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       catalog_name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)

        return JsonResponse({'result': 1})

    elif table_name == '二级目录':
        # 获取点击的库名并转换成英文
        db = con(us_china)
        cursor = db.cursor()

        sql = """select id from AdminSecond where chinese_abb='{0}'""".format(catalog_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        sql_id = cursor.fetchall()
        for ids in sql_id:
            id = ids[0]

        sql = """select first_id from AdminSecond where chinese_abb='{0}'""".format(catalog_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        first_ids = cursor.fetchall()
        for first_i in first_ids:
            first_id = first_i[0]

        sql = """delete from AdminThird where second_id = {0} ;""".format(id)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)

        sql = """delete from AdminSecond where chinese_abb='{0}' and first_id={1};""".format(catalog_name, first_id)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "删除二级目录"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               catalog_name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       catalog_name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)

        return JsonResponse({'result': 1})
    elif table_name == '三级目录':
        # 获取点击的库名并转换成英文
        db = con(us_china)
        cursor = db.cursor()

        sql = """select second_id from AdminThird where chinese_abb='{0}'""".format(catalog_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        sql_id = cursor.fetchall()
        for ids in sql_id:
            id = ids[0]

        sql = """delete from AdminThird where chinese_abb='{0}' and second_id={1};""".format(catalog_name, id)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "删除三级目录"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               catalog_name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       catalog_name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)

        return JsonResponse({'result': 1})


# 三级目录更新操作
def update_catalog(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    firstId_list = []
    secondId_list = []
    thirdId_list = []
    result = []
    sendlog = ''
    update_name = request.POST.get('update_name')
    us_name = getPinyin(update_name)
    table_name = request.POST.get('dier')
    old_name = request.POST.get('old_name')
    depart = request.session.get('depart')
    depname = depart
    us_china = getPinyin(depart)
    if table_name == '一级目录':
        # 获取点击的库名并转换成英文
        db = con(us_china)
        # print(db)
        cursor = db.cursor()
        sql = """select id from AdminFirst where chinese_abb='{0}'""".format(old_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        first_tuple = cursor.fetchall()
        for f_tup in first_tuple:
            for first_id in f_tup:
                firstId_list.append(first_id)

        sql = """update AdminFirst set chinese_abb='{0}' where id={1};""".format(update_name, firstId_list[0])
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        
        sql = """update AdminFirst set department='{0}'  where id={1};""".format(us_name, firstId_list[0])
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)

        db.commit()
        db.close()

        task = "修改一级目录"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               update_name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       update_name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)
        us_updateName = getPinyin(update_name)
        result.append({'result': 1, 'us_updateName': us_updateName})

        return JsonResponse({'result': result})

    elif table_name == '二级目录':
        # 获取点击的库名并转换成英文
        db = con(us_china)
        cursor = db.cursor()

        sql = """select first_id from AdminSecond where chinese_abb='{0}'""".format(old_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        first_ids = cursor.fetchall()
        for first_i in first_ids:
            first_id = first_i[0]

        sql = """select id from AdminSecond where chinese_abb='{0}'""".format(old_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        second_tuple = cursor.fetchall()
        for s_tup in second_tuple:
            for second_id in s_tup:
                secondId_list.append(second_id)

        sql = """update AdminSecond set chinese_abb='{0}' where id={1} ;""".format(update_name, secondId_list[0])
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        
        sql = """update AdminSecond set  industry ='{0}' where id={1} ;""".format(us_name, secondId_list[0])
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "修改二级目录"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               update_name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       update_name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)

        us_updateName = getPinyin(update_name)
        result.append({'result': 1, 'us_updateName': us_updateName})

        return JsonResponse({'result': result})

    elif table_name == '三级目录':
        # 获取点击的库名并转换成英文
        db = con(us_china)
        # print(db)
        cursor = db.cursor()
        sql = """select second_id from AdminThird where chinese_abb='{0}';""".format(old_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        sql_id = cursor.fetchall()
        for ids in sql_id:
            id = ids[0]

        sql = """select id from AdminThird where chinese_abb='{0}';""".format(old_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        third_tuple = cursor.fetchall()
        for t_tup in third_tuple:
            for third_id in t_tup:
                secondId_list.append(third_id)

        sql = """update AdminThird set chinese_abb='{0}' where id={1} ;""".format(update_name, secondId_list[0])
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        
        sql = """update AdminThird set species='{0}' where id={1} ;""".format(us_name, secondId_list[0])
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "修改三级目录"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        # depart = request.session.get('depart')
        # us_china = getPinyin(depart)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               update_name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       update_name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)
        us_updateName = getPinyin(update_name)
        result.append({'result': 1, 'us_updateName': us_updateName})

        return JsonResponse({'result': result})


# 管理操作页面
def admin_operation(request):

    depart = request.session.get('depart')
    username = request.POST.get("username")
    us_china = getPinyin(depart)
    db = con(us_china)
    cursor = db.cursor()
    if request.method == "POST":
        url_config = request.POST.get("req_config")
        # 增加用户
        if url_config == "add_username":
            # print(username)
            sql = """select username from Auser where username='{0}';""".format(username)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            select_name = cursor.fetchall()
            if select_name:
                return JsonResponse({'result': 0})
            sql = """insert into Auser values (null, "{0}");""".format(username)

        # 删除用户
        elif url_config == "del_username":
            username = request.POST.get("username")
            sql = """delete from Auser where username = "{0}";""".format(username)

        # 增加服务目录
        elif url_config == "add_server":
            serviceName = request.POST.get("serviceName")
            hosts = request.POST.get("hosts")
            uris = request.POST.get("uris")
            upstream_url = request.POST.get("upstream_url")
            sql = """select serviceName from Aservice where serviceName='{0}';""".format(serviceName)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            service_name = cursor.fetchall()
            if service_name:
                return JsonResponse({'result': 0})
            sql = """insert into Aservice values (null, "{0}","{1}","{2}","{3}");""".format(serviceName,hosts, uris,upstream_url)

        # 删除服务
        elif url_config == "del_server":
            serviceName = request.POST.get("serviceName")
            sql = """delete from Aservice where serviceName = "{0}";""".format(serviceName)

        # 添加组
        elif url_config == "add_group":
            group = request.POST.get("group")
            username = request.POST.get("username")
            sql = """select group from Agroup where group='{0}';""".format(group)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            group_name = cursor.fetchall()
            if group_name:
                return JsonResponse({'result': 0})
            sql = """insert into Agroup values (null, "{0}","{1}");""".format(group, username)
        # 删除组
        elif url_config == "add_group":
            group = request.POST.get("group")
            sql = """delete from Agroup where group = "{0}";""".format(group)
        # 添加acl
        elif url_config == "add_acl":
            serviceName = request.POST.get("serviceName")
            name = request.POST.get("name")
            whitelist = request.POST.get("whitelist")
            sql = """insert into Aacl values (null, "{0}","{1}","{2}");""".format(serviceName, name, whitelist)
        # 删除acl
        elif url_config == "del_acl":
            serviceName = request.POST.get("serviceName")
            sql = """delete from Aacl where serviceName = "{0}";""".format(serviceName)
        # 添加控制
        elif url_config == "add_control":
            name = request.POST.get("name")
            day = request.POST.get("day")
            serviceName = request.POST.get("serviceName")
            consumer_id = "11cd88d2-3e6a-464f-8dc3-5c1a42e8c54b"
            sql = """insert into Acontrols values (null, "{0}","{1}","{2}","{3}");""".format(name, day, serviceName, consumer_id)

        # 删除控制
        elif url_config == "del_control":
            serviceName = request.POST.get("serviceName")
            sql = """delete from Acontrols where serviceName = "{0}",id = "{0}";""".format(serviceName, id)
        # sql格式
        sql_ending = sql.encode(encoding="utf8")
        # print(sql)
        try:
            # 执行sql语句
            cursor.execute(sql_ending)
            # 提交到数据库执行
            db.commit()

            return JsonResponse({"result": 1})
        except:
            # 如果发生错误则回滚
            db.rollback()

            return JsonResponse({"result": 0})


# 添加部门即创建库
def add_depart(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    departname = ''
    sendlog = ''
    if request.method == "POST":
        depart = request.POST.get("depart")
        print(depart)
        db = con('test')
        cursor = db.cursor()
        sql = """select group_name from dm_group where name='{0}';""".format(depart)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        group_name = cursor.fetchall()[0][0]
        sql = """select * from department where dataname='{0}';""".format(group_name)

        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        department = cursor.fetchall()
        db.close()
        if department:
            return JsonResponse({"result": 0})
        else:
            db = con('test')
            cursor = db.cursor()
            sql = """select group_name,hosts  from dm_group where name='{0}';""".format(depart)
            print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            departhost = cursor.fetchall()
            departname = departhost[0][0]
            host = departhost[0][1]
            print(departname, '--部门名称', host, '--映射域名')
            db.commit()
            db.close()

            depart_en = getPinyin(departname)
            sub_obj = db_con()
            print(sub_obj)
            # 查询mysql中的所有库
            print(depart_en, '--库名')
            sql_add_database = 'create database {0} default character set utf8 COLLATE utf8_general_ci;\n exit \n'.format(depart_en)
            print(sql_add_database)
            sql_ending = sql_add_database.encode(encoding="utf8")
            sub_obj.stdin.write(sql_ending)
            sub_obj.stdin.close()
            time.sleep(3)
            add_sql = sub_sql(depart_en)
            print(add_sql)
            subprocess.Popen(add_sql, shell=True)
            sub_obj.stdin.close()
            db = con('test')
            cursor = db.cursor()
            time.sleep(8)
            if db:
                # 获取ogCode
                sql = """select org_no from  dm_group where name='{0}';""".format(depart)
                print(sql)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                ogCodes = cursor.fetchall()
                ogCode = ogCodes[0][0]
                # ogCode = 'sadfghjkwertyuityu'
                time.sleep(2)

                sql = """insert into department values (null,'{0}','{1}','{2}','{3}');""".format(departname, depart_en, host, ogCode)
                print(sql)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                db.commit()
                # 关闭数据库连接
                db.close()

                task = "创建部门"
                endtime = time.time()
                timeArray = time.localtime(endtime)
                endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                db = con("test")
                cursor = db.cursor()
                sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                                       depart,
                                                                                                       "超级管理员",
                                                                                                       airTime,
                                                                                                       endtime,
                                                                                    "成功")
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                db.commit()
                db.close()
                sendlog = str((task,
                               depart,
                               "超级管理员",
                               airTime,
                               endtime,
                               '成功'))
                sendLog = send_log(sendlog)

                return JsonResponse({"result": 1})


# 用户接入
def user_login(request):
    # 判断数据库是否存在
    host_list = []
    data = request.POST.get('user_login_name')
    database = Department.objects.filter(dataname=data)
    if database:
        us_china = getPinyin(data)
        db = con(us_china)
        cursor = db.cursor()
        sql = """select hosts from BasicInter;"""
        sql_ending = sql.encode(encoding="utf8")
        # 执行sql语句
        cursor.execute(sql_ending)
        hosts = cursor.fetchall()
        for set_host in hosts:
            host = set_host[0]
            host_list.append({'host': host, 'us_china': us_china})

        return JsonResponse({"result": host_list})
    else:
        return JsonResponse({"result": 0})


# 用户操作页面
# 向数据库增加用户信息
def user_operation(request):
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    user_login_name = request.session.get('depart')
    us_china = getPinyin(user_login_name)
    # print(user_login_name,'*'*1000)
    print(user_login_name)
    depname = user_login_name
    isTrue = True
    # 打开数据库连接
    # 判断数据库是否存在
    res = []
    uri = ''
    uris = ''
    task = ''
    name_obj = ''
    temp_val = ''
    apikey=''
    interface_name = ''
    username = request.POST.get("username")
    us_china = getPinyin(user_login_name)
    sendlog = ''

    if request.method == "POST":
        url_config = request.POST.get("req_config")
        # 增加用户
        if url_config == "add_username":
            task="添加用户"
            db = con('test')
            cursor = db.cursor()
            sql = """select username from Uuser where username='{0}';""".format(username)
            print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            select_name = cursor.fetchall()
            print(select_name)
            if select_name:
                return JsonResponse({'result': 0})
            xml_obj = xml.dom.minidom.parse('./url_config/add_username.xml')
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
                xml_obj = xml.dom.minidom.parse('./url_config/req_apikey.xml')
                root = xml_obj.documentElement
                url = root.getElementsByTagName('url')[0].firstChild.data
                method = root.getElementsByTagName('requests')[0].firstChild.data
                username = request.POST.get("username")
                params = {"username": username}
                res = requests.request(method=method,
                                       url=url,
                                       params=params)
                res_dict = json.loads(res.text)
                apikey = res_dict["result"]
            except requests.exceptions.ReadTimeout:
                xml_obj = xml.dom.minidom.parse('./url_config/req_apikey.xml')
                root = xml_obj.documentElement
                url = root.getElementsByTagName('url')[0].firstChild.data
                method = root.getElementsByTagName('requests')[0].firstChild.data
                username = request.POST.get("username")
                params = {"username": username}
                res = requests.request(method=method,
                                       url=url,
                                       params=params)
                res_dict = json.loads(res.text)
                apikey = res_dict["result"]
            # apikey='sdfhjklhgfdsafh'

            sql = """insert into Uuser values (null,'{0}','{1}','{2}');""".format(username, apikey, us_china)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            db.commit()
            db.close()
            #   添加安全目录数据用户
            obj = user.objects.create(id=None,
                                      username=username,
                                      api_key=apikey,
                                      )
            obj.save(using='Safe_dic')
            endtime = time.time()
            timeArray = time.localtime(endtime)
            endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

            db = con("test")
            cursor = db.cursor()
            sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                                   username,
                                                                                                   user_login_name,
                                                                                                   airTime,
                                                                                                   endtime,
                                                                                                   "成功")
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            db.commit()
            db.close()
    
            sendlog = str((task,
                           username,
                           user_login_name,
                           airTime,
                           endtime,
                           '成功'))
            sendLog = send_log(sendlog)
            print(sendlog)
            print(sendLog.wait())
            xml_obj = xml.dom.minidom.parse('./url_config/add_group.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            params = {"group": username,
                      "username": username,
                      }
            try:
                res = requests.request(method=method,
                                       url=url,
                                       data=params,
                                       timeout=0.5)
            except requests.exceptions.ConnectionError:
                isTrue = False
                print(isTrue)
            except requests.exceptions.ReadTimeout:
                isTrue = False
                print(isTrue)
            if isTrue == False:
                isTrue =True
                return JsonResponse({"result": 1})

        # 删除用户
        elif url_config == "del_username":
            db = con('test')
            cursor = db.cursor()
            groupName_list = ''
            type_name = ''
            userName = request.POST.get("username")
            name_obj = userName
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
            task = "删除用户"
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
            sql = """select hosts from department where dataname='{0}';""".format(user_login_name)
            print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            hosts = cursor.fetchall()[0][0]
            print(hosts)
            db.close()
            db = con(us_china)
            cursor = db.cursor()
            upstream_urls = ''
            serviceName = request.POST.get("serviceName")
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
                #print(sql)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                service_name = cursor.fetchall()
                #print(service_name)
                if service_name:
                    res.append({"host": hosts, "user_login_name": user_login_name, "result": 0, "uri": uri,
                                "temp_val": temp_val})
                    return JsonResponse({"result": res})
                sql = """insert into Uservice values (null, "{0}","{1}","{2}","{3}","{4}");""".format(serviceName,
                                                                                                hosts, uris,client_type,
                                                                                                type)
            else:
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
                # interface_name = type_name + '=' + type
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
                                                                                                hosts, uris, client_type, type)

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
           
            # print(uris,hosts,upstream_urls)
            xml_obj = xml.dom.minidom.parse('./url_config/add_server.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            data = {"serviceName": serviceName,
                    "hosts": hosts,
                    "uris": uris,
                    "upstream_url": upstream_urls
                    }
            print(data)
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
            db = con(us_china)
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
            group = request.POST.get("group")
            userName = request.POST.get("username")
            db = con(us_china)
            cursor = db.cursor()
            sql = """select groupName from Ugroup where groupName='{0}';""".format(group)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            group_name = cursor.fetchall()
            if group_name:
                return JsonResponse({"result": 0})
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
            db = con(us_china)
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
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            uacl_list = cursor.fetchall()
            print(uacl_list, '%' * 100)
            if uacl_list:
                return JsonResponse({'result': 0})
            else:
                sql = """insert into Uacl values (null, "{0}","{1}","{2}");""".format(serviceName, aclName,
                                                                                      whitelist)
                #  添加安全目录数据访问了控制
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
                print(url,method,params,'*'*100)
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
            db = con(us_china)
            cursor = db.cursor()
            serviceName = request.POST.get("serviceName")
            print(1,serviceName)
            name_obj = serviceName
            xml_obj = xml.dom.minidom.parse('./url_config/del_acl.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            # id = get_service_id(serviceName)
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
            db = con(us_china)
            cursor = db.cursor()
            name = request.POST.get("name")
            day = request.POST.get("day")
            serviceName = request.POST.get("serviceName")
            name_obj = serviceName
            userName = request.POST.get('username')
          #  with open("./sql_file/id.txt", "r") as f:
           #     con_id = f.readlines()
            #    for consu_id in con_id:
             #       cons_id = consu_id.split(' ')
              #      if cons_id[0] == userName:
               #         consumer_id = cons_id[1]
           # print(consumer_id)
           # print(name,serviceName,userName,day)
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
                                                                                                      day)
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
                params = {"name": name,
                          "day": day,
                          "serviceName": serviceName,
                          "username": username,
                          }
                try:
                    res = requests.request(method=method,
                                           url=url,
                                           data=params,
                                           timeout=0.5)
                    task = "添加流量控制"
                except requests.exceptions.ConnectionError:
                    isTrue = False
                    task = "添加流量控制"
                except requests.exceptions.ReadTimeout:
                    isTrue = False
                    task = "添加流量控制"

        # 删除控制
        elif url_config == "del_control":
            db = con(us_china)
            cursor = db.cursor()
            userName = request.POST.get('username')
            serviceName = request.POST.get("serviceName")
            name_obj = serviceName
            # 删除安全目录流量控制
            print(username,serviceName)
            #obj = FlowControl.objects.filter(username=userName, serviceName=serviceName)
            #obj.delete()
            sql = """delete from Ucontrols where serviceName = "{0}";""".format(serviceName)
            xml_obj = xml.dom.minidom.parse('./url_config/del_control.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            #id = get_service_id(serviceName)
            print(url,username,serviceName)
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

        # sql格式
        # print(isTrue)
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
                    res.append({"host": hosts,
                                "user_login_name": getPinyin(user_login_name),
                                "result": 1,
                                "uri": uri,
                                "temp_val": temp_val,
                                })
                    print(res)
                    return JsonResponse({"result": res})
                else:
                    return JsonResponse({"result": 1})
            except:
                # 如果发生错误则回滚
                db.rollback()
                return JsonResponse({"result": 0})


# 获取映射域名存到数据库
def realm(request):
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con('test')
    cursor = db.cursor()
    realm = request.POST.get('realm')

    sql = """update department set hosts='{0}' where dataname='{1}';""".format(realm, depart)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    # 关闭数据库连接
    db.close()
    # 打印日志
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    task = '修改映射域名'
    name_obj = realm
    depname = depart
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                           name_obj,
                                                                                           depname,
                                                                                           airTime,
                                                                                           endtime,
                                                                                           "成功")
    print(sql)
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

    return JsonResponse({"result": 1})


# 映射目录显示页面
def admin_mapping(request):

    realm_list = ''
    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con('test')
    # db = pymysql.connect('127.0.0.1', 'root', 'root', us_china, charset='utf8')
    cursor = db.cursor()
    sql = """select hosts from department where dataname='{0}';""".format(depart)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_realm = cursor.fetchall()
    # realm_list = set_realm[0][0]
    for realm in set_realm:
        realm_list = realm[0]
    print(realm_list)
    # 提交到数据库执行
    db.commit()
    # 关闭数据库连接
    db.close()

    return render(request, 'superAdmin/admin_mapping.html', {'realm': realm_list})


def user_getfirst(request):

    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con(us_china)
    # print(china_db,'%'*100)
    first_list = []
    cursor = db.cursor()
    sql = """select chinese_abb from AdminFirst ;"""
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

    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con(us_china)
    second_list = []
    first = request.POST.get("first")
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
    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con(us_china)
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


# db数据目录展示页面
def db_list(request):

    tb_name = []
    field_info = []
    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con(us_china)
    # print(db)
    cursor = db.cursor()
    sql = """select * from savetable;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    table_list = cursor.fetchall()
    for tableName in table_list:
        tb_name.append({"tablename":tableName[1],"us_tablename":tableName[2]})
    sql = """select * from add_field;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    field_list = cursor.fetchall()
    for field in field_list:
        field_info.append({'fieldName':field[1], 'fieldDesc':field[2], 'fieldType': field[3]})

    return render(request, 'superAdmin/db_list.html', {'tb_name': tb_name, 'field_info': field_info})


# 添加sql选项卡
def page_Sql(request):

    return render(request, 'superAdmin/page_Sql.html')


# 添加sql选项卡
def sql_name(request):

    return render(request, 'superAdmin/sql_name.html')


# 生成sql页面
def sql_append(request):

    return render(request, 'superAdmin/sql_append.html')


# # sql语句保存操作
# def sql_save(request):
#     sql_name = request.POST.get('sql_name')
#     get_sql = request.POST.get('get_sql')
#     sql_ip = request.POST.get('sql_ip')
#     depart = request.session.get('depart')
#     print(sql_name, get_sql, sql_ip)
#     print(depart)
#
#     # if sql_name == '' or get_sql == '':
#     #     return JsonResponse({'res': 0})
#     #     # print(sql_name, sql)
#     # else:
#         # 获取点击的库名并转换成英文
#     us_china = getPinyin(depart)
#     db = con(us_china)
#     cursor = db.cursor()
#     sql = """select dbName from dbList where dbName='{0}';""".format(sql_name)
#     print(sql)
#     sql_ending = sql.encode(encoding="utf8")
#     cursor.execute(sql_ending)
#     select_name = cursor.fetchall()
#     if select_name:
#         return JsonResponse({'result': 0})
#     else:
#         sql = """insert into dbList values(null, '{0}', '{1}','{2}', 0);""".format(sql_name, sql,sql_ip)
#         sql_ending = sql.encode(encoding="utf8")
#         cursor.execute(sql_ending)
#         db.commit()
#         db.close()
#         return JsonResponse({'result': 1})


# sql语句保存操作
def sql_save(request):

    depname = request.POST.get('depname')
    sql_name = request.POST.get('sql_name')
    sql = request.POST.get('get_sql')
    print(sql,'111111111111111111111111111111111111111111111111111')
    sql1 = sql.replace(",", "$")
    sql_ip = request.POST.get('sql_ip')
    # print(sql_ip, '%'*100)
    sqlIp = ""
    user_login_name = request.session.get('depart')
    print(sql_name, sql, sql_ip, user_login_name)
    if sql_name == '' or sql == '':
        return JsonResponse({'res': 0})
    else:
        i = 0
        with open("./sql_file/count.txt", "r") as f:
            strcount = f.read()
            i = int(strcount)
        # if "bass" in sql_ip:
        #     sqlIp1 = sql_ip.replace("bass","1.255.1.202")
        #     sqlIp = sqlIp1 + '?id={0}'.format(str(i))
        if sql_ip == 'mysql':
            sqlIp1 = "http://1.255.1.202:3000/api/db"
            sqlIp = sqlIp1 + '?id={0}'.format(str(i))
        elif sql_ip == 'oracle':
            sqlIp1 = "http://1.255.1.202:3001/api/db"
            sqlIp = sqlIp1 + '?id={0}'.format(str(i))
        elif sql_ip == '国家接口':
            sqlIp1 = "http://1.255.1.202:3002/api/db"
            sqlIp = sqlIp1 + '?id={0}'.format(str(i))
        elif sql_ip == '易鲸捷':
            sqlIp1 = "http://1.255.1.150:3003/api/db"
            sqlIp = sqlIp1 + '?id={0}'.format(str(i))
        elif sql_ip == 'sqlServer':
            sqlIp1 = "http://1.255.1.202:3004/api/db"
            sqlIp = sqlIp1 + '?id={0}'.format(str(i))
        elif sql_ip == '达梦':
            sqlIp1 = "http://1.255.1.202:3005/api/db"
            sqlIp = sqlIp1 + '?id={0}'.format(str(i))
        elif sql_ip == '南大通用':
            sqlIp1 = "http://1.255.1.202:3006/api/db"
            sqlIp = sqlIp1 + '?id={0}'.format(str(i))
        elif sql_ip == '人大金仓':
            sqlIp1 = "http://1.255.1.202:3007/api/db"
            sqlIp = sqlIp1 + '?id={0}'.format(str(i))
        else:
            sqlIp1 = "http://1.255.1.202:3008/api/db"
            sqlIp = sqlIp1 + '?id={0}'.format(str(i))
        with open("./sql_file/db.search.sql", "a+") as f:
            f.write(sql1 + "\n")
        strI = str(i + 1)
        with open("./sql_file/count.txt", "w") as f:
            f.write(strI)
        cmd = "/root/datalink/copyfile.sh"
        readCmd = os.system(cmd)
        print(readCmd)
        print(111)
        # 获取点击的库名并转换成英文
        us_china = getPinyin(user_login_name)
        db = con(us_china)
        # print(db)
        cursor = db.cursor()
        sql = """insert into dbList values(null, '{0}', '{1}','{2}', 0);""".format(sql_name, sql, sqlIp)
        print(sql, '&' * 100)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()
        with open("./sql_file/db.detail.sql", "a+") as f:
            detail="桥接名称："+ sql_name +"  "+"数据区："+sql_ip+"  "+"sql语句："+sql1
            f.write(detail+"\n")
        return JsonResponse({'result': 1})


# 数据桥接修改
def sql_update(request):

    dbname = request.POST.get("dbname")
    sql_name = request.POST.get("sql_name")
    sql_ip = request.POST.get("sql_ip")
    get_sql = request.POST.get("get_sql")
    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con(us_china)
    cursor = db.cursor()
    sql = """update dbList set dbName='{0}',dbSql='{1}',dbIP='{2}' where dbName='{3}'""".format(sql_name, get_sql, sql_ip, dbname)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    return JsonResponse({"result": 1})


# 删除sql语句
def delete_db(request):

    delete_name = request.POST.get('delete_name')
    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con(us_china)
    cursor = db.cursor()
    sql = """delete from dbList where dbName='{0}';""".format(delete_name)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    return JsonResponse({'result': 1})


# 服务目录跳转
def data_uri(request, data, uri):
    temp_val = request.session.get('temp_val')

    return render(request, 'superAdmin/temp_val.html', {'temp_val': temp_val})


# 服务目录传参
def service_type(request):

    temp_val = request.POST.get('temp_val')
    request.session['temp_val'] = temp_val
    return JsonResponse({'res': 1})


# 修改acl
def update_acl(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sername = request.POST.get('sername')
    newSerName = request.POST.get('newSerName')
    newWL = request.POST.get('newWL')
    depart = request.session.get('depart')
    depname = depart
    us_china = getPinyin(depart)
    db = con(us_china)
    cursor = db.cursor()
    # 删除acl
    sql = """delete from Uacl where serviceName='{0}';""".format(sername)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    obj = AccessControl.objects.filter(serviceName=sername)
    obj.delete()
    # 添加acl
    sql = """insert into Uacl values (null,'{0}','acl','{1}');""".format(newSerName, newWL)
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
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                           newSerName,
                                                                                           depname,
                                                                                           airTime,
                                                                                           endtime,
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

    return JsonResponse({'result': 1})


# 修改流量控制
def update_control(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    name = "rate-limiting"
    username = request.POST.get('username')
    serviceName = request.POST.get('old_serviceName')
    newSerName = request.POST.get('newusername')
    newvicName = request.POST.get('servicename')
    consumer_id = '11cd88d2-3e6a-464f-8dc3-5c1a42e8c54b'
    newday = request.POST.get('day')
    depart = request.session.get('depart')
    depname = depart
    us_china = getPinyin(depart)
    db = con(us_china)
    cursor = db.cursor()
    # 删除流量控制
    sql = """delete from Ucontrols where userName= '{0}' and serviceName = "{1}";""".format(username, serviceName)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    obj = FlowControl.objects.filter(username=username,serviceName=serviceName)
    obj.delete()
    # 添加流量控制
    sql = """insert into Ucontrols values (null, "{0}","{1}","{2}","{3}","{4}");""".format(name, newSerName, consumer_id, newvicName, newday)
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
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                           serviceName,
                                                                                           depname,
                                                                                           airTime,
                                                                                           endtime,
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

    return JsonResponse({'result': 1})


# 修改用户名
def update_username(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    username = request.POST.get('old_name')
    newSerName = request.POST.get('update_name')
    china_db = request.session.get('depart')
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)
    cursor = db.cursor()
    # 删除用户名
    # sql = """select groupName from Ugroup where userName = '{0}';""".format(sername)
    # sql_ending = sql.encode(encoding="utf8")
    # cursor.execute(sql_ending)
    # set_groupName = cursor.fetchall()
    # for groupName in set_groupName:
    #     groupName_list = groupName[0]
    # if groupName_list:
    #     sql = """delete from Ugroup where userName = '{0}'""".format(sername)
    #     sql_ending = sql.encode(encoding="utf8")
    #     cursor.execute(sql_ending)

    sql = """select userName from Uuser where userName='{0}';""".format(newSerName)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    usersname = cursor.fetchall()
    if usersname:
        return JsonResponse({'result': 0})
    sql = """delete from Uuser where userName = "{0}";""".format(username)
    # 删除安全目录用户
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    obj = User.objects.filter(username=username)
    obj.delete()
    # 添加用户名

    sql = """insert into Uuser values (null, "{0}");""".format(newSerName)
    print(sql)
    #   添加安全目录数据用户
    task = "修改用户"
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()
    obj = User.objects.create(id=None,
                              username=newSerName,
                              api_key='',
                              )

    obj.save(using='Safe_dic')
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con('test')
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                           newSerName,
                                                                                           china_db,
                                                                                           airTime,
                                                                                           endtime,
                                                                                           "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    cursor.close()
    db.close()

    sendlog = str((task,
                   newSerName,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({'result': 1})


def update_service(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    res = []
    sendlog = ''
    depart = request.session.get('depart')
    depname = depart
    user_login_name = getPinyin(depart)
    firstSel = request.POST.get('firstSel')
    secondSel = request.POST.get('secondSel')
    thirdSel = request.POST.get('thirdSel')
    serviceName = request.POST.get('old_serviceName')
    service_Name = request.POST.get('serviceName')
    type = request.POST.get('type_content')
    type_name = request.POST.get('type')
    client_type = request.POST.get('client_type')
    upstream_url = request.POST.get('add_upstream_url')

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
    sql = """select hosts from department where dataname='{0}';""".format(depart)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    hosts = cursor.fetchall()[0][0]
    print(hosts,)
    db.close()

    db = con(user_login_name)
    cursor = db.cursor()

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
        # sql = """select serviceName from Uservice where serviceName='{0}';""".format(service_Name)
        # sql_ending = sql.encode(encoding="utf8")
        # cursor.execute(sql_ending)
        # ser_name = cursor.fetchall()
        # print(ser_name)
        # if ser_name:
        #     return JsonResponse({'result': 0})
        sql = """insert into Uservice values (null, "{0}","{1}","{2}","{3}","{4}");""".format(service_Name, hosts, uris, client_type,
                                                                                        type)
    else:
        interface_name = type_name + '=' + type
        uris = '/' + getPinyin(firstSel) + '/' + getPinyin(
            secondSel) + '/' + type_name + '/' + getPinyin(thirdSel) + '/' + upstream_url
        # temp_val = type_name + '=' + type
        # uri = '/' + getPinyin(firstSel) + '/' + getPinyin(secondSel) + '/' + type_name + '/' + getPinyin(
        #     thirdSel) + '/' + 'xxx?' + type_name
        # 去重
        # sql = """select serviceName from Uservice where serviceName='{0}';""".format(service_Name)
        # sql_ending = sql.encode(encoding="utf8")
        # cursor.execute(sql_ending)
        # service_name = cursor.fetchall()
        # if service_name:
        #     return JsonResponse({'result': 0})
        sql = """insert into Uservice values (null, "{0}","{1}","{2}","{3}","{4}");""".format(service_Name,
                                                                                        hosts,
                                                                                        uris,client_type,
                                                                                        type)
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
    sql = """insert into commonlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               service_Name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                           service_Name,
                                                                                           depname,
                                                                                           airTime,
                                                                                           endtime,
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


# 文件通道
def admin_file(request):

    file_list = []
    china_db = request.session.get('depart')
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)
    cursor = db.cursor()
    sql = """select * from fileName"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_sql = cursor.fetchall()
    for file_set in set_sql:
        # print(file_set,'$'*100)
        file_list.append(file_set[1])
    # print(file_list,'$'*100)
    return render(request, 'superAdmin/admin_file.html', {'file_list': file_list})


# 消息通道
def admin_ways(request):

    message_list = []
    china_db = request.session.get('depart')
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)
    cursor = db.cursor()
    sql = """select * from messageName"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_sql = cursor.fetchall()
    for message_set in set_sql:
        message_list.append(message_set[1])

    return render(request, 'superAdmin/admin_ways.html', {'message_list': message_list})


# 接口通道
def admin_interface(request):

    interface_list = []
    china_db = request.session.get('depart')
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)
    cursor = db.cursor()
    sql = """select * from interfaceName"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_sql = cursor.fetchall()
    for interface_set in set_sql:
        interface_list.append(interface_set[1])
    print(interface_list)

    return render(request, 'superAdmin/admin_interface.html', {'interface_list': interface_list})


# 将四大通道数据添加到对应数据库中
def type_add(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    type = request.POST.get('type')
    add_name = request.POST.get('name')
    print(add_name)
    dataIp = request.POST.get('dataIP')
    china_db = request.session.get('depart')
    depname = china_db
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)
    cursor = db.cursor()
    # print(type, '*'*100)
    if type == 'file':
        sql = """select fileName from fileList where fileName='{0}';""".format(add_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        select_name = cursor.fetchall()
        if select_name:
            return JsonResponse({'result': 0})
        print(add_name)
        sql = """insert into fileList values(null,'{0}','{1}',  0);""".format(add_name, dataIp)
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "插入文件"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               add_name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       add_name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)

        return JsonResponse({'result': 1})

    elif type == 'interface':
        sql = """select interfaceName from interfaceList where interfaceName='{0}';""".format(add_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        select_name = cursor.fetchall()
        if select_name:
            return JsonResponse({'result': 0})

        sql = """insert into interfaceList values(null,'{0}', '{1}',  0);""".format(add_name, dataIp)
        # print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "插入接口"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               add_name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       add_name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)

        return JsonResponse({'result': 1})
    elif type == 'ways':
        sql = """select messageName from messageList where messageName='{0}';""".format(add_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        select_name = cursor.fetchall()
        if select_name:
            return JsonResponse({'result': 0})
        sql = """insert into messageList values(null,'{0}', '{1}',  0);""".format(add_name, dataIp)
        # print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "插入消息"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               add_name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       add_name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)

        return JsonResponse({'result': 1})


def add_feild(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    feild_name = request.POST.get('feild_name')
    feild_desc = request.POST.get('feild_desc')
    feild_type = request.POST.get('feild_typelen')
    feild_key = request.POST.get('feild_key')
    sendlog = ''
    china_db = request.session.get('depart')
    print('部门',china_db)
    depname = china_db
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)
    cursor = db.cursor()
    sql = """select fieldName from add_field where fieldName='{0}';""".format(feild_name)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    field_name = cursor.fetchall()
    print(field_name)
    if field_name:
        return JsonResponse({'result': 0})
    sql = """insert into add_field values(null,'{0}','{1}','{2}','{3}',0);""".format(feild_name, feild_desc, feild_type, feild_key)
    task = "添加字段"
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con('test')
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                           feild_name,
                                                                                           depname,
                                                                                           airTime,
                                                                                           endtime,
                                                                                           "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    cursor.close()
    db.close()

    sendlog = str((task,
                   feild_name,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({'result': 1})


def get_data_log(request):

    role = request.POST.get("role")
    list1 = []
    if role == "superAdmin":
        # database = request.POST.get('database')
        db = con("test")
        cursor = db.cursor()
        sql1 = """select * from mylog order by superAirtime desc; """
        sql_ending = sql1.encode(encoding="utf8")
        cursor.execute(sql_ending)
        set_sql = cursor.fetchall()
        for sql_two in set_sql:
            list1.append({"task": sql_two[1],
                          "obj": sql_two[2],
                          "user": sql_two[3],
                          "starttime": sql_two[4],
                          "endtime": sql_two[5],
                          "status": sql_two[6]})
        cursor.close()
        db.close()

        return JsonResponse({"result": list1})
    if role == "departmentAdmin":

        database = request.POST.get('database')
        db = con(database)
        cursor = db.cursor()
        sql1 = """select * from departlog order by detartAirtime desc;"""
        sql_ending = sql1.encode(encoding="utf8")
        cursor.execute(sql_ending)
        set_sql = cursor.fetchall()
        print(set_sql)
        for sql_two in set_sql:
            list1.append({"task": sql_two[1],
                          "obj": sql_two[2],
                          "user": sql_two[3],
                          "starttime": sql_two[4],
                          "endtime": sql_two[5],
                          "status": sql_two[6]})
        cursor.close()
        db.close()

        return JsonResponse({"result": list1})

    if role == "commonUser":

        database = request.POST.get('database')
        db = con(database)
        cursor = db.cursor()
        sql1 = """select * from commonlog order by detartAirtime desc;"""
        sql_ending = sql1.encode(encoding="utf8")
        cursor.execute(sql_ending)
        set_sql = cursor.fetchall()
        print(set_sql)
        for sql_two in set_sql:
            list1.append({"task": sql_two[1],
                          "obj": sql_two[2],
                          "user": sql_two[3],
                          "starttime": sql_two[4],
                          "endtime": sql_two[5],
                          "status": sql_two[6]})
        cursor.close()
        db.close()
        print(list1)

        return JsonResponse({"result": list1})


def journal(request):

    return render(request, 'superAdmin/journal.html')

# timeStamp = 1381419600
# timeArray = time.localtime(timeStamp)
# otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
# print(otherStyleTime


def get_data(request):

    if request.method == "POST":
        role = request.POST.get("role")
        list1=[]
        if role == "superAdmin":
            # database = request.POST.get('database')
            db = con("test")
            cursor = db.cursor()
            sql1 = """select * from mylog; """
            # sql1 = """select * from mylog;"""
            sql_ending = sql1.encode(encoding="utf8")
            cursor.execute(sql_ending)
            set_sql = cursor.fetchall()
            for sql_two in set_sql:
                list1.append({"task": sql_two[1],
                              "obj": sql_two[2],
                              "user": sql_two[3],
                              "starttime": sql_two[4],
                              "endtime": sql_two[5],
                              "status": sql_two[6]})
            cursor.close()
            db.close()

            return JsonResponse({"result": list1})

        if role == "departmentAdmin":
            database = request.POST.get('database')
            db = con(database)
            cursor = db.cursor()
            sql1 = """select * from departlog;"""
            sql_ending = sql1.encode(encoding="utf8")
            cursor.execute(sql_ending)
            set_sql = cursor.fetchall()
            print(set_sql)
            for sql_two in set_sql:
                list1.append({"task": sql_two[1],
                              "obj": sql_two[2],
                              "user": sql_two[3],
                              "starttime": sql_two[4],
                              "endtime": sql_two[5],
                              "status": sql_two[6]})
            cursor.close()
            db.close()

            return JsonResponse({"result":list1})

        if role == "commonUser":
            print(1)
            database = request.POST.get('database')
            db = con(database)
            cursor = db.cursor()
            sql1 = """select * from commonlog;"""
            sql_ending = sql1.encode(encoding="utf8")
            cursor.execute(sql_ending)
            set_sql = cursor.fetchall()
            print(set_sql)
            for sql_two in set_sql:
                list1.append({"task": sql_two[1],
                              "obj": sql_two[2],
                              "user": sql_two[3],
                              "starttime": sql_two[4],
                              "endtime": sql_two[5],
                              "status": sql_two[6]})
            cursor.close()
            db.close()

            return JsonResponse({"result": list1})


# 数据源修改表名
def update_table(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    china_db = request.session.get('depart')
    old_table_ch = request.POST.get("old_table_ch")
    print(old_table_ch)
    depname = china_db
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)
    # print(old_table_en,"*"*100)
    table_ch = request.POST.get("table_ch")
    table_en = request.POST.get("table_en")

    # 连接点击的数据库
    cursor = db.cursor()
    # sql = """select tableName from savetable where tableName='{0}';""".format(table_ch)
    # print(sql)
    # sql_ending = sql.encode(encoding="utf8")
    # cursor.execute(sql_ending)
    # user_name = cursor.fetchall()
    # print(user_name)
    # if user_name:
    #     return JsonResponse({'result': 0})
    sql = """update savetable set tableName='{0}',us_tableName='{1}' where tableName='{2}';""".format(table_ch, table_en, old_table_ch)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    task = "修改数据表"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                           table_ch,
                                                                                           depname,
                                                                                           airTime,
                                                                                           endtime,
                                                                                           "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   table_ch,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({'result': 1})


# 数据源修改字段
def update_field(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    old_field_name = request.POST.get("old_fieldname")
    field_name = request.POST.get("field_name")
    field_desc = request.POST.get("field_desc")
    field_type = request.POST.get("field_type")
    sendlog = ''
    # 连接点击的数据库
    china_db = request.session.get('depart')
    depname = china_db
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)
    cursor = db.cursor()

    sql = """select tableKey_id from add_field where fieldName='{0}';""".format(old_field_name)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    tables = cursor.fetchall()
    for table in tables:
        table_id = table[0]

    sql = """update add_field set fieldName='{0}',fieldDesc='{1}',fieldType='{2}' where fieldName='{3}';""".format(field_name, field_desc, field_type, old_field_name)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    task = "修改字段"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                           field_name,
                                                                                           depname,
                                                                                           airTime,
                                                                                           endtime,
                                                                                           "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   field_name,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({"result": 1})


# 管理员页面添加数据表
def add_table(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    table_ch = request.POST.get('table_ch')
    table_en = request.POST.get('table_en')
    china_db = request.session.get('depart')
    depname = china_db
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)
    cursor = db.cursor()
    sql = """select tableName from savetable where tableName='{0}';""".format(table_ch)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    service_name = cursor.fetchall()
    if service_name:
        return JsonResponse({'result': 0})
    sql = """insert into savetable values(null, '{0}', '{1}', 0);""".format(table_ch, table_en)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    task = "添加表名"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                           table_ch,
                                                                                           depname,
                                                                                           airTime,
                                                                                           endtime,
                                                                                           "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   table_ch,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({'result': 1})


# 管理员页面添加字段操作
def add_field(request):
     
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    table_name = request.POST.get('table_name')
    field_name = request.POST.get('field_name')
    field_desc = request.POST.get('field_desc')
    field_type = request.POST.get('field_type')
    china_db = request.session.get('depart')
    depname = china_db
    print(depname)
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)

    # 连接点击的数据库
    cursor = db.cursor()
    sql = """select id from savetable where  us_tableName='{0}';""".format(table_name)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    dbs = cursor.fetchall()[0][0]
    print(dbs,'*'*200)
    sql = """select fieldName from add_field where fieldName='{0}' and tableKey_id={1};""".format(field_name, dbs)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    select_name = cursor.fetchall()
    print(select_name)
    if select_name:
        return JsonResponse({'result': 0})
    sql = """insert into add_field values(null, '{0}', '{1}', '{2}', 0, '{3}');""".format(field_name, field_desc, field_type, dbs)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    task = "添加字段"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                           field_name,
                                                                                           depname,
                                                                                           airTime,
                                                                                           endtime,
                                                                                           "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   field_name,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({'result': 1})


# 页面显示字段信息
def field_show(request):

    field_info = []
    tableName = request.POST.get('tableName')
    china_db = request.session.get('depart')
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)
    cursor = db.cursor()
    sql = """select id from savetable where  us_tableName='{0}';""".format(tableName)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    dbs = cursor.fetchall()[0][0]
    print(dbs)
    sql = """select * from add_field where tableKey_id={0};""".format(dbs)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    field_list = cursor.fetchall()
    for field in field_list:
        field_info.append({'fieldName': field[1], 'fieldDesc': field[2], 'fieldType': field[3]})

    return JsonResponse({'result': field_info})


# 数据源删除数据表
def table_delete(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    tb_id = ''
    sendlog = ''
    table_en = request.POST.get('table_en')
    china_db = request.session.get('depart')
    depname = china_db
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)
    cursor = db.cursor()
    sql = """select id from savetable where us_tableName='{0}';""".format(table_en)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    tb_id = cursor.fetchall()[0][0]
    print(tb_id)
    sql = """delete from add_field where tableKey_id={0};""".format(tb_id)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    sql = """delete from savetable where us_tableName='{0}';""".format(table_en)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    task = "删除数据表"
    print(task)
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                           table_en,
                                                                                           depname,
                                                                                           airTime,
                                                                                           endtime,
                                                                                           "成功")
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   table_en,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({'result': 1})


# 数据源删除字段操作
def field_delete(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    field_name = request.POST.get('fieldname')
    china_db = request.session.get('depart')
    depname = china_db
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)
    cursor = db.cursor()

    sql = """select tableKey_id from add_field where fieldName='{0}';""".format(field_name)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    table_ids = cursor.fetchall()
    for table_ids in table_ids:
        table_id = table_ids[0]

    sql = """delete from add_field where fieldName='{0}' and tableKey_id={1};""".format(field_name, table_id)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    task = "删除字段"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                           field_name,
                                                                                           depname,
                                                                                           airTime,
                                                                                           endtime,
                                                                                           "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   field_name,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({'result': 1})


#  修改三大通道类型
def update_type(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    type = request.POST.get('type')
    old_name = request.POST.get('old_name')
    update_name = request.POST.get('update_name')
    update_dataIP = request.POST.get('update_dataIP')
    # print(add_name, '*' * 100)
    china_db = request.session.get('depart')
    depname = china_db
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)
    cursor = db.cursor()
    print(type)
    # print(type, '*'*100)
    if type == 'file':
        sql = """delete from fileList where fileName='{0}';""".format(old_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        # sql = """select fileName from fileList where fileName='{0}';""".format(update_name)
        # sql_ending = sql.encode(encoding="utf8")
        # cursor.execute(sql_ending)
        # file_name = cursor.fetchall()
        # if file_name:
        #     return JsonResponse({'result': 0})
        sql = """insert into fileList values(null,'{0}','{1}',  0);""".format(update_name, update_dataIP)
        # print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "修改文件"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con('test')
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               update_name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       update_name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)

        return JsonResponse({'result': 1})
    elif type == 'interface':
        sql = """delete from interfaceList where interfaceName='{0}';""".format(old_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        # sql = """select interfaceName from interfaceList where interfaceName='{0}';""".format(update_name)
        # sql_ending = sql.encode(encoding="utf8")
        # cursor.execute(sql_ending)
        # select_name = cursor.fetchall()
        # if select_name:
        #     return JsonResponse({'result': 0})
        sql = """insert into interfaceList values(null,'{0}','{1}',  0);""".format(update_name, update_dataIP)
        # print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "修改接口"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               update_name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       update_name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)

        return JsonResponse({'result': 1})
    elif type == 'ways':
        sql = """delete from messageList where messageName='{0}';""".format(old_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        # sql = """select messageName from messageList where messageName='{0}';""".format(update_name)
        # sql_ending = sql.encode(encoding="utf8")
        # cursor.execute(sql_ending)
        # select_name = cursor.fetchall()
        # if select_name:
        #     return JsonResponse({'result': 0})
        sql = """insert into messageList values(null,'{0}','{1}',  0);""".format(update_name, update_dataIP)
        # print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "修改消息"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               update_name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       update_name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)

        return JsonResponse({'result': 1})


# 删除三大通道
def del_type(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    type = request.POST.get('type')
    name = request.POST.get('name')
    print(type)
    china_db = request.session.get('depart')
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    depname = china_db
    db = con(us_china)
    cursor = db.cursor()
    if type == 'file':
        sql = """delete from fileList where fileName='{0}';""".format(name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "删除文件"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)
        return JsonResponse({'result': 1})
    elif type == 'interface':
        sql = """delete from interfaceList where interfaceName='{0}';""".format(name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "删除接口"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)

        return JsonResponse({'result': 1})
    elif type == 'message':
        sql = """delete from messageList where messageName='{0}';""".format(name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "删除消息"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                               name,
                                                                                               depname,
                                                                                               airTime,
                                                                                               endtime,
                                                                                               "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()
        sendlog = str((task,
                       name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)

        return JsonResponse({'result': 1})


# select生成页面
def sql_admin(request):

    db_list = []
    # 获取点击的库名并转换成英文
    china_db = request.session.get('depart')
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)
    # print(db)
    cursor = db.cursor()
    # 获取一级目录列表
    sql = 'select * from dbList;'
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    dbs = cursor.fetchall()
    for db in dbs:
        dbIP = db[3]+'/api/db?id='+str(db[0])
        db_list.append({'dbName': db[1], 'dbSql': db[2], 'dbIP': dbIP})

    return render(request, 'superAdmin/sql_admin.html', {'db_list': db_list})


#sql写入文件
def update_data(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    # 连接点击的数据库
    china_db = request.session.get('depart')
    depname = china_db
    us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(us_china)
    cursor = db.cursor()
    sql1 = """select dbSql from dbList"""
    sql_ending = sql1.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_sql_one = cursor.fetchall()
    with open("./sql_file/select_sql.sql", "w") as f:
        f.truncate()
    for sql_two in set_sql_one:
        for sql in sql_two:
            if sql == "":
                pass
            else:
                with open("./sql_file/select_sql.sql", "a+") as f:
                    f.write(sql + "\n")
    cursor.close()
    db.close()

    task = "sql文件写入"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,
                                                                                           field_name,
                                                                                           depname,
                                                                                           airTime,
                                                                                           endtime,
                                                                                           "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   field_name,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({'result': 1})


# sql页面获取数据
def get_table(request):
    get_table = []
    result = []
    china_db = request.session.get('depart')
    # depname = china_db
    us_china = getPinyin(china_db)
    print(china_db)
    db = con(us_china)
    cursor = db.cursor()
    sql = """select tableName from savetable;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    getTables = cursor.fetchall()
    for getTable in getTables:
        get_table.append(getTable)

    # sql = """select fieldName,fieldDesc from add_field ;"""
    # sql_ending = sql.encode(encoding="utf8")
    # cursor.execute(sql_ending)
    # field_list = cursor.fetchall()
    # for field in field_list:
    #     get_table.append({'fieldName': field[0], 'fieldDesc': field[1]})
    # result.append({"getTable":getTable,})
    # print(get_table)
    return JsonResponse({'result': get_table})


def desc_show(request, db_name):
    # db_name = []
    db_id = ''
    us_table = []
    field_info = []
    # us_china = getPinyin(china_db)
    # 连接点击的数据库
    print(db_name)
    china_db = request.session.get('depart')
    us_china = getPinyin(china_db)
    db = con(us_china)
    cursor = db.cursor()
    sql = """select id,us_tableName from savetable where  tableName='{0}';""".format(db_name)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    dbs = cursor.fetchall()
    for db in dbs:
        db_id = db[0]
        us_table.append(db[1])
    print(db_id,'#'*100)
    print(dbs[0],"*"*100)
    sql = """select * from add_field where tableKey_id={0};""".format(db_id)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    field_list = cursor.fetchall()
    for field in field_list:
        print(field)
        field_info.append({'fieldName': field[1], 'fieldDesc': field[2], 'field_type': field[3], "us_table": us_table})

    return JsonResponse({'data': field_info})


# 三级目录获取修改之前默认值
def get_datadier(request):

    catalog_list = []
    depname = request.POST.get('depname')
    print(depname)
    erji = request.POST.get('erji')
    sanji = request.POST.get('sanji')
    siji = request.POST.get('siji')
    print(erji, sanji, siji, depname, '*' * 100)
    en_name = getPinyin(depname)
    print(en_name,'*'*100)
    db = con(en_name)
    cursor = db.cursor()
    sql = """select chinese_abb from AdminFirst where department='{0}';""".format(erji)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_first_name = cursor.fetchall()
    print(set_first_name)
    catalog_list.append({'first_name': set_first_name[0][0]})
    print(set_first_name,'*'*100)
    sql = """select chinese_abb from AdminSecond where industry='{0}';""".format(sanji)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_second_name = cursor.fetchall()
    catalog_list.append({'second_name': set_second_name[0][0]})
    sql = """select chinese_abb from AdminThird where species='{0}';""".format(siji)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_third_name = cursor.fetchall()
    catalog_list.append({'third_name': set_third_name[0][0]})
    db.close()
    print(catalog_list,'*'*100)

    return JsonResponse({'result': catalog_list})


def check_user_apikey(request):

    if request.method == "POST":
        list_user = []
        username = request.POST.get('username')
        if username:
            database = request.POST.get('database')
            db = con(database)
            cursor = db.cursor()
            sql1 = """select apikey from Uuser WHERE username='{0}'; """.format(username)
            sql_ending = sql1.encode(encoding="utf8")
            cursor.execute(sql_ending)
            set_sql = cursor.fetchall()
            for sql_two in set_sql:
                print(sql_two)
                list_user.append({"username": username, "apikey": sql_two[0]})
            cursor.close()
            db.close()
            return JsonResponse({"result":list_user}, content_type='application/json;charset=utf-8')
        else:
            database = request.POST.get('database')
            db = con(database)
            cursor = db.cursor()
            sql1 = """select * from Uuser; """
            sql_ending = sql1.encode(encoding="utf8")
            cursor.execute(sql_ending)
            set_sql = cursor.fetchall()
            print(set_sql)
            for sql_two in set_sql:
                list_user.append({"username": sql_two[1], "apikey": sql_two[2]})
            cursor.close()
            db.close()
            print(list_user)

            return JsonResponse({"result": list_user}, content_type='application/json; charset=utf-8')


def datalink(request):

    if request.method == "POST":
        i = 0
        with open("./sql_file/count.txt","r") as f:
            strcount = f.read()
            i = int(strcount)
        isflag = True
        depart = ''
        visitCount = request.POST.get('visitCount')
        columns = request.POST.get('columns')
        resourceName = request.POST.get('resourceName')
        processId= request.POST.get('processId')
        resourceId = request.POST.get('resourceId')
        ogCode = request.POST.get('ogCode')

        # 通过ogCode获取部门名
        db = con("test")  # 链接库
        cursor = db.cursor()
        sql = """select dataname from department where ogCode = '{0}';""".format(ogCode)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        depart = cursor.fetchall()[0][0]
        db.commit()
        db.close()
        print("部门获取成功")

        # 添加用户
        xml_obj = xml.dom.minidom.parse('./url_config/add_username.xml')
        root = xml_obj.documentElement
        url = root.getElementsByTagName('url')[0].firstChild.data
        method = root.getElementsByTagName('requests')[0].firstChild.data
        params = {"username": processId}
        try:
            res = requests.request(method=method,
                                   url=url,
                                   data=params,
                                   timeout=0.5)
        except requests.exceptions.ConnectionError:
            isflag = False
        except requests.exceptions.ReadTimeout:
            isflag = False
        if isflag == False:
            isflag = True
            print("添加用户成功")

            # 部门插入表

            apikey = get_apikey(processId)
            db = con("test")
            cursor = db.cursor()
            sql = """insert into Uuser values (null,'{0}','{1}','{2}');""".format(
                processId,apikey,depart)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            db.commit()
            db.close()
            print("部门用户表插入成功")
            
            # 三大目录插入用户
            db = con("Safe_dic")
            cursor = db.cursor()
            sql = """insert into user values (null,'{0}','{1}');""".format(
                processId,apikey)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            db.commit()
            db.close()
            print("三大目录用户插入成功")

            # 添加组
            xml_obj = xml.dom.minidom.parse('./url_config/add_group.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            params = {"group": processId,
                      "username": processId,
                      }
            try:
                res = requests.request(method=method,
                                       url=url,
                                       data=params,
                                       timeout=0.5)
            except requests.exceptions.ConnectionError:
                isflag = False
            except requests.exceptions.ReadTimeout:
                isflag = False
            if isflag == False:
                isflag =True
                print("添加组成功")

                # 查询sql
                us_depart = getPinyin(depart)
                db = con(us_depart)  # �~S��~N���~S
                cursor = db.cursor()
                sql = """select dbsql from dbList where dbName = '{0}';""".format(resourceName)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                table_data = cursor.fetchall()[0]
                select = table_data[0]
                print(select)
                db.commit()
                db.close()
         
                print("查询sql成功")
                parrten = re.compile(r"from (.*);")
                table= re.findall(parrten, select)[0]
                print(table)
                # 获取三级目录
                us_depart=getPinyin(depart)
                db = con(us_depart)  # 链接库
                cursor = db.cursor()
                sql = """select uris from Uservice where upstream_url = '{0}';""".format(resourceName)
                print(sql)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                serviceData = cursor.fetchall()[0][0]
                print(serviceData)
                # 关闭数据库连接
                db.close()
                print("获取uris成功")

                # 添加dbList
                sqlIp = 'http://1.255.1.202:3000/api/db?id={0}'.format(str(i))
                listcolumns = eval(columns)
                briName = "table." + ".".join(str(i) for i in listcolumns) + processId
                field = "$".join(str(i) for i in listcolumns)
                sql_yuju = "select {0} from {1};".format(field, table)
                db = con(us_depart)
                cursor = db.cursor()
                sql = """insert into dbList VALUES (null,'{0}','{1}','{2}',0)""".format(briName, sql_yuju, sqlIp)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                db.commit()
                db.close()
                print("添加新dbList成功")

                # 拆分三级目录在拆分
                serviceData_split = serviceData.split("/")
                serviceData_split[-1] = resourceId+processId
                newserviceData = "/".join(str(i) for i in serviceData_split)
                # 添加CSB服务
                xml_obj = xml.dom.minidom.parse('./url_config/add_server.xml')
                root = xml_obj.documentElement
                url = root.getElementsByTagName('url')[0].firstChild.data
                method = root.getElementsByTagName('requests')[0].firstChild.data
                # 上架服务
                serName = resourceId + processId

                data = {"serviceName": serName,
                        "hosts": us_depart+".gz",
                        "uris": newserviceData,
                        "upstream_url": sqlIp,
                        }
                try:
                    res = requests.request(method=method,
                                           url=url,
                                           data=data,
                                           timeout=1)
                except requests.exceptions.ReadTimeout:
                    isflag = False
                except requests.exceptions.ConnectionError:
                    isflag = False

                if isflag == False:
                    print("服务添加成功")
                    with open ("./sql_file/db.search.sql","a+") as f:
                        f.write(sql_yuju+"\n")
                    strI = str(i + 1)
                    with open("./sql_file/count.txt","w") as f:
                        f.write(strI)

                    # 向部门Uservice插入数据
                    hosts = us_depart + '.gz'
                    db = con(us_depart)
                    cursor = db.cursor()
                    serName = resourceId + processId
                    print(newserviceData)
                    sql = """insert into Uservice VALUES (null,'{0}','{1}','{2}','{3}')""".format(serName, hosts, newserviceData, briName)
                    print(sql)
                    sql_ending = sql.encode(encoding="utf8")
                    cursor.execute(sql_ending)
                    db.commit()
                    db.close()
                    print("插入部门数据成功")
                
                    #数据目录添加
                    db = con("Data_dic")
                    cursor = db.cursor()
                    serName = resourceId + processId
                    sql = """insert into dataname VALUES (null,'{0}','{1}','{2}','{3}','{4}','{5}','{6}',0)""".format(serName,
                                                                                                                      hosts,
                                                                                                                      serviceData_split[1],
                                                                                                                      serviceData_split[2],
                                                                                                                      serviceData_split[4],
                                                                                                                      serviceData_split[3],
                                                                                                                      briName)
                    print(sql)
                    sql_ending = sql.encode(encoding="utf8")
                    cursor.execute(sql_ending)
                    db.commit()
                    db.close()
                    print("添加三大目录数据成功")

                    # 插入acl
                    serName = resourceId + processId
                    xml_obj = xml.dom.minidom.parse('./url_config/add_acl.xml')
                    root = xml_obj.documentElement
                    url = root.getElementsByTagName('url')[0].firstChild.data
                    method = root.getElementsByTagName('requests')[0].firstChild.data
                    params = {"serviceName": serName,
                              "name": "acl",
                              "whitelist": processId,
                              }
                    try:
                        res = requests.request(method=method,
                                               url=url,
                                               data=params,
                                               timeout=0.5)
                    except requests.exceptions.ConnectionError:
                        isflag = False
                    except requests.exceptions.ReadTimeout:
                        isflag = False
                    if isflag == False:
                        isflag = True
                        print("CSBacl成功")
                        # 插入部门acl
                        db = con(us_depart)
                        cursor = db.cursor()
                        serName = resourceId + processId
                        sql = """insert into Uacl VALUES (null,'{0}','{1}','{2}')""".format(serName, "acl", processId)
                        sql_ending = sql.encode(encoding="utf8")
                        cursor.execute(sql_ending)
                        db.commit()
                        db.close()
                        print("插入部门acl成功")

                        # 插入三大目录acl
                        db = con("Safe_dic")
                        cursor = db.cursor()
                        serName = resourceId + processId
                        sql = """insert into accesscontrol VALUES (null,'{0}','{1}','{2}')""".format(serName, "acl", processId)
                        sql_ending = sql.encode(encoding="utf8")
                        cursor.execute(sql_ending)
                        db.commit()
                        db.close()
                        print("插入三大目录acl成功")
                        url = "http://" + us_depart+".gz" + newserviceData

                        return JsonResponse({"apikey": apikey, "url": url})


def get_apikey(username):

    xml_obj = xml.dom.minidom.parse('./url_config/req_apikey.xml')
    root = xml_obj.documentElement
    url = root.getElementsByTagName('url')[0].firstChild.data
    method = root.getElementsByTagName('requests')[0].firstChild.data
    print(username)
    params = {"username": username}
    res = requests.request(method=method,
                           url=url,
                           data=params)
    res_dict = json.loads(res.text)
    result = res_dict.get("result")

    return result


def request_apikey(request):

    if request.method == "GET":
        username = request.GET.get("username")
        print(username)
        db = con("test")
        cursor = db.cursor()
        sql = """select api_key from Uuser where username='{0}';""".format(username)
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()
        apikey = cursor.fetchall()[0][0]
        print(apikey)
        dict1 = {"username": username, "apikey": apikey}
        result = str(dict1)
        return HttpResponse(result, content_type='application/json; charset=utf-8')


def userGroupApikey(request):
    if request.method == "POST":

        isflag = True
        username = request.POST.get('username')
        ogCode = request.POST.get('ogCode')

        xml_obj = xml.dom.minidom.parse('./url_config/add_username.xml')
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
            isflag = False
        except requests.exceptions.ReadTimeout:
            isflag = False
        if isflag == False:
            isflag = True
           
            db = con("test")
            cursor = db.cursor()
            sql = """select group_name from dm_group where org_no = '{0}'""".format(ogCode)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            db.commit()
            db.close()
            depart = cursor.fetchall()[0][0]
            apikey = get_apikey(username)
            db = con("test")
            cursor = db.cursor()
            sql = """insert into Uuser values (null,'{0}','{1}','{2}');""".format(username, apikey, depart)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            db.commit()
            db.close()
            print("部门用户表插入成功")

            # 三大目录插入用户
            db = con("Safe_dic")
            cursor = db.cursor()
            sql = """insert into user values (null,'{0}','{1}');""".format(username, apikey)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            db.commit()
            db.close()
            print("三大目录插入成功")

            xml_obj = xml.dom.minidom.parse('./url_config/add_group.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            params = {"group": username,
                      "username": username,
                      }
            try:
                res = requests.request(method=method,
                                       url=url,
                                       data=params,
                                       timeout=0.5)
            except requests.exceptions.ConnectionError:
                isflag = False
            except requests.exceptions.ReadTimeout:
                isflag = False
            if isflag == False:
                isflag = True
                print("添加组成功")
                db = con("test")
                cursor = db.cursor()
                sql = """select api_key from Uuser where username='{0}';""".format(username)
                print(sql)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                db.commit()
                db.close()
                apikey = cursor.fetchall()[0][0]
                print(apikey)
                dict1 = {"username": username, "apikey": apikey}
                result = str(dict1)

                return HttpResponse(result, content_type='application/json; charset=utf-8')


# 状态日志页面显示
def status_journal(request):

    staIP = ''
    staTime = ''
    staMethod = ''
    staDataList = ''
    staUser = ''
    staStatus = ''
    staDataSize = ''
    staClient = ''
    status_log = get_status()
    print(status_log.wait())
    sta_log = status_log.stdout.read()
    status_log.stdin.close()
    status_log.stdout.close()
    staLog = eval(sta_log)
    sta_Log = (staLog.get('results'))
    print(sta_Log)
    try:
        for statusLog in sta_Log:
            status_Log = statusLog.get("payload")
            statuslog = status_Log.strip().split(" ")
            print(statuslog)
            staIP = statuslog[0]
            print(staIP)
            staMethod = statuslog[3]
            print(staMethod)
            staDataList = statuslog[4]
            print(staDataList)
            db = con("test")
            cursor = db.cursor()
            sql= """select uris from Uservice;"""
            sql_ending=sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            staData=cursor.fetchall()
            print(staData)
            for Datena in staData:
                Data=Datena[0]
                if Data in staDataList:
                    staDataList=Data
            sql = """select ServiceName from Uservice where uris='{0}';""".format(staDataList)
            print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            staDataName = cursor.fetchall()[0][0]
            print(staDataName)
            staUser = statuslog[5]
            print(staUser)
            staDataSize = statuslog[8]
            print(staDataSize)
            staClient = statuslog[10]
            print(staClient)
            staStatus = statuslog[6] + ' ' + statuslog[7]
            print(staStatus)
            staTime = statuslog[1][1:]
            monthdic = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
            timespilt= staTime.split("/")
            timespilt[1] = monthdic[timespilt[1]]
            print(timespilt)
            year = timespilt[2].split(":")
            print(year)
            formatTime = year[0]+'-'+timespilt[1]+'-'+timespilt[0]+' '+ year[1]+':'+year[2]+':'+year[3]
            print(formatTime)
            staTime = datetime.datetime.strptime(formatTime, '%Y-%m-%d %H:%M:%S')
            print(staTime)
            data = staIP, staTime, staMethod, staDataList, staUser, staStatus, staDataSize, staClient
            print(data, 'data' * 100)
            db = con('test')
            cursor = db.cursor()
            sql = """insert into stalog values (null,'{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}');""".format(staIP,
                                                                                                                 staTime,
                                                                                                                 staMethod,
                                                                                                                 staDataName,
                                                                                                                 staDataList,
                                                                                                                 staUser,
                                                                                                                 staStatus,
                                                                                                                 staDataSize,
                                                                                                                 staClient)
            print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            db.commit()
            db.close()
    except:
        pass
    return render(request, 'superAdmin/status_journal.html')


# 统计分析页面显示
def statistical_analysis(request):

    return render(request, 'superAdmin/statistical_analysis.html')


def getTotalTop(request):
    if request.method =="POST":
        staIP = ''
        staTime = ''
        staMethod = ''
        staDataList = ''
        staUser = ''
        staStatus = ''
        staDataSize = ''
        staClient = ''
        status_log = get_status()
        sta_log = status_log.stdout.read()
        status_log.stdin.close()
        status_log.stdout.close()
        staLog = eval(sta_log)
        sta_Log = (staLog.get('results'))
        print(sta_Log)
        try:
            for statusLog in sta_Log:
                status_Log = statusLog.get("payload")
                statuslog = status_Log.strip().split(" ")
                print(statuslog)
                staIP = statuslog[0]
                print(staIP)
                staMethod = statuslog[3]
                print(staMethod)
                staDataList = statuslog[4]
                db = con("test")
                cursor = db.cursor()
                sql = """select ServiceName from Uservice where uris='{0}';""".format(staDataList)
                print(sql)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                staDataName = cursor.fetchall()[0][0]
                print(staDataList)
                staUser = statuslog[5]
                print(staUser)
                staDataSize = statuslog[8]
                print(staDataSize)
                staClient = statuslog[10]
                print(staClient)
                staStatus = statuslog[6] + ' ' + statuslog[7]
                print(staStatus)
                staTime = statuslog[1][1:]
                monthdic = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
                timespilt= staTime.split("/")
                timespilt[1] = monthdic[timespilt[1]]
                print(timespilt)
                year = timespilt[2].split(":")
                print(year)
                formatTime = year[0]+'-'+timespilt[1]+'-'+timespilt[0]+' '+ year[1]+':'+year[2]+':'+year[3]
                print(formatTime)
                staTime = datetime.datetime.strptime(formatTime, '%Y-%m-%d %H:%M:%S')
                print(staTime)
                print(staTime)
                data = staIP, staTime, staMethod, staDataList, staUser, staStatus, staDataSize, staClient
                print(data, 'data' * 100)
                db = con('test')
                cursor = db.cursor()
                sql = """insert into stalog values (null,'{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}');""".format(
                    staIP,
                    staTime,
                    staMethod,
                    staDataName,
                    staDataList,
                    staUser,
                    staStatus,
                    staDataSize,
                    staClient)
                print(sql)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                db.commit()
                db.close()
        except:
            pass
        HttpStatus=[]
        client=[]
        dayTop=[]
        totalTop = []
        ipServiceCount=[]
        db = con('test')
        cursor = db.cursor()
        sql = """select staDataName,count(1) as count from stalog group by staDataName order by count desc limit 10;"""
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        dataNum = cursor.fetchall()

        for data in dataNum:
            print(data)
            dict = {"data":data[0],"num":data[1]}
            print(dict)
            totalTop.append(dict)
            print(totalTop)

        db = con('test')
        cursor = db.cursor()
        sql = """SELECT s.staDataName,count(1) as listcount FROM stalog s where s.staTime>= Now() - interval 24 hour GROUP BY s.staDataName ORDER BY listcount DESC LIMIT 10;"""
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        dataNum = cursor.fetchall()

        for data in dataNum:
            print(data)
            dict = {"data": data[0], "num": data[1]}
            print(dict)
            dayTop.append(dict)
        print(dayTop)

        db = con('test')
        cursor = db.cursor()
        sql = """select staClient,count(1) as count from stalog group by staClient having count(1)>=1;"""
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        clientResult = cursor.fetchall()

        for data in clientResult:
            print(data)
            dict = {"data": data[0], "num": data[1]}
            print(dict)
            client.append(dict)
        print(client)

        db = con('test')
        cursor = db.cursor()
        sql = """select staStatus,count(1) as count from stalog group by staStatus having count(1)>=1;"""
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        HttpResult = cursor.fetchall()

        for data in HttpResult:
            print(data)
            dict = {"data": data[0], "num": data[1]}
            print(dict)
            HttpStatus.append(dict)
        print(HttpStatus)

        db = con('test')
        cursor = db.cursor()
        sql = """SELECT s.staDataName,count(1) as listcount,s.staIP FROM stalog s group by staDataName,staIP having count(1)>=1;"""
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        IpServer = cursor.fetchall()

        for data in IpServer:
            print(data)
            dict = {"data": data[0], "num": data[1],"ip":data[2]}
            print(dict)
            ipServiceCount.append(dict)
        print(ipServiceCount)
        db.close()

        return JsonResponse({"totalTop":totalTop,"dayTop":dayTop,"client":client,"httpstatus":HttpStatus,"ipServiceCount":ipServiceCount})



# 文件源录入页面显示
def file_list(request):

    file_name = []
    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con(us_china)
    cursor = db.cursor()
    sql = """select * from fileName;"""
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    filename = cursor.fetchall()
    for file_Name in filename:

        file_name.append(file_Name[1])
    print(file_name)
    db.close()
    # print(file_Name[1])

    return render(request, 'superAdmin/file_list.html', {'file_name': file_name})


# 接口源录入页面显示
def interface_list(request):

    interface_name = []
    depart = request.session.get('depart')
    us_china = getPinyin(depart)
    db = con(us_china)
    cursor = db.cursor()
    sql = """select * from interfaceName;"""
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    interfacename = cursor.fetchall()
    for interface_Name in interfacename:
        interface_name.append(interface_Name[1])
    print(interface_name)
    db.close()

    return render(request, 'superAdmin/interface_list.html', {'interface_name': interface_name})


# 消息源录入页面显示
def message_list(request):

    message_name = []
    depart = request.session.get('depart')  # 部门
    us_china = getPinyin(depart)
    db = con(us_china)
    cursor = db.cursor()
    sql = """select * from messageName;"""
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    messagename = cursor.fetchall()
    for message_Name in messagename:
        message_name.append(message_Name[1])
    print(message_name)
    db.close()

    return render(request, 'superAdmin/message_list.html', {'message_name': message_name})


# 获取元数据参数
def meta_list(request):

    depname = request.POST.get('depname')  # 部门
    metatype = request.POST.get('metatype')  # 数据元表（接口、文件、消息）
    mename = request.POST.get('tableName')  # 数据元名称
    print(depname)
    print(metatype)
    print(mename)
    meta_params = []
    metatable = ''
    metaname = ''
    meta_id = ''
    partable = ''

    if metatype == 'file':
        metatable = 'fileName'
        metaname = 'file_name'
        partable = 'fileParams'
        meta_id = 'filename_id_id'
    elif metatype == 'interface':
        metatable = 'interfaceName'
        metaname = 'interface_name'
        partable = 'interfaceParams'
        meta_id = 'interface_id_id'
    elif metatype == 'message':
        metatable = 'messageName'
        metaname = 'message_name'
        partable = 'messageParams'
        meta_id = 'message_id_id'

    us_china = getPinyin(depname)
    db = con(us_china)
    cursor = db.cursor()

    sql = """select id from {0} where {1}='{2}';""".format(metatable, metaname, mename)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    me_id = cursor.fetchall()[0][0]
    print(me_id)

    sql = """select * from {0} where {1} = {2};""".format(partable, meta_id, me_id)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    metatype = cursor.fetchall()
    for meta_type in metatype:
        print(meta_type)
        meta_params.append({'fieldName': meta_type[1], 'fieldDesc': meta_type[2], 'fieldType': meta_type[3]})
    print(meta_params)
    db.close()

    return JsonResponse({"result": meta_params})


# 添加元数据名称
def add_meta(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    depname = request.POST.get('depname')  # 部门
    metatype = request.POST.get('metatype')  # 数据元表（接口、文件、消息）
    tableName = request.POST.get('table_ch')  # 数据元名称
    metatable = ''
    file_name = ''
    task = ''
    print(depname)
    print(metatype)
    print(tableName)

    if metatype == 'file':
        metatable = 'fileName'
        metaname = 'file_name'
        task = "添加文件源名称"
    elif metatype == 'interface':
        metatable = 'interfaceName'
        metaname = 'interface_name'
        task = "添加接口源名称"
    elif metatype == 'message':
        metatable = 'messageName'
        metaname = 'message_name'
        task = "添加消息源名称"

    us_china = getPinyin(depname)
    db = con(us_china)
    cursor = db.cursor()
    # 添加类型时去重
    sql = """select {0} from {1} where {2}='{3}';""".format(metaname, metatable, metaname, tableName)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    type_content = cursor.fetchall()
    print(type_content, '*'*100)
    if type_content:
        return JsonResponse({'result': 0})
    else:
        sql = """insert into {0} values (null,'{1}');""".format(metatable, tableName)
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, tableName,
                                                                                               depname,
                                                                                               airTime, endtime, "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       tableName,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)

        return JsonResponse({'result': 1})


# 添加元数据参数
def add_params(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    depname = request.POST.get('depname')  # 部门
    metatype = request.POST.get('metatype')  # 数据元表（文件、接口、通道）
    mename = request.POST.get('table_name')  # 数据元名称
    par_name = request.POST.get('field_name')  # 参数名称
    par_desc = request.POST.get('field_desc')  #　参数描述
    par_type = request.POST.get('field_type')  # 参数类型

    metatable = ''
    metaname = ''
    partable = ''
    task = ''
    print(depname)
    print(metatype)
    print(par_name)
    print(par_desc)
    print(par_type)

    if metatype == 'file':
        metatable = 'fileName'
        metaname = 'file_name'
        partable = 'fileParams'
        task = "添加文件源参数"
    elif metatype == 'interface':
        metatable = 'interfaceName'
        metaname = 'interface_name'
        partable = 'interfaceParams'
        task = "添加接口源参数"
    elif metatype == 'message':
        metatable = 'messageName'
        metaname = 'message_name'
        partable = 'messageParams'
        task = "添加消息源参数"
    print(metatable)
    print(metaname)
    print(partable)

    us_china = getPinyin(depname)
    db = con(us_china)
    cursor = db.cursor()
    sql = """select {0} from {1} where {2}='{3}'""".format(metaname, partable, metaname, par_name)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    type_content = cursor.fetchall()
    print(type_content,'*'*100)
    if type_content:
        return JsonResponse({'result': 0})
    else:
        sql = """select id from {0} where {1}='{2}';""".format(metatable, metaname, mename)
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        me_id = cursor.fetchall()[0][0]
        print(me_id)

        sql = """insert into {0} values (null,'{1}','{2}','{3}',{4});""".format(partable, par_name, par_desc, par_type, me_id)
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, par_name,
                                                                                               depname,
                                                                                               airTime, endtime, "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       par_name,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)

        return JsonResponse({'result': 1})


#修改sql语句
def update_Sql(request):
    if request.method == "POST":
        depname = request.POST.get("depname")
        newsql = request.POST.get("new_sql")
        oldsql = request.POST.get("old_sql")
        print(depname,newsql,oldsql)
        database = getPinyin(depname)
        with open("./sql_file/db.search.sql","r") as f:
            sql_list = f.readlines()
            print(sql_list)
            for sql in sql_list:
                print(sql)
                if oldsql in sql:
                    print(1)
                    list_index = [i for i, x in enumerate(sql_list) if x == oldsql +"\n"][0]
                    print(list_index)
                    sql_list[list_index]= newsql+"\n"
                    with open("./sql_file/db.search.sql","w") as f:
                        print(sql_list)
                        for sql in sql_list:
                            f.write(sql)

        replaceNewsql = newsql.replace("$",",")
        replaceOldsql = oldsql.replace("$",",")

        db = pymysql.connect('127.0.0.1',
                             'root',
                             'root',
                             database,
                             charset='utf8')
        cursor = db.cursor()
        sql = "update dbList as a inner join dbList as b on a.id = b.id set a.dbSql = '{0}' where a.dbSql = '{1}';".format(replaceNewsql,replaceOldsql)
        print(sql)

        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        return JsonResponse({"result":1})

# 修改数据元名称
def meta_update(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    depname = request.POST.get('depname')  # 部门
    metatype = request.POST.get('metatype')
    mename = request.POST.get('old_table_ch')  # 数据元名称
    newmename = request.POST.get('table_ch')  # 新的数据元名称
    metatable = ''
    metable = ''
    task = ''
    print(depname)
    print(metatype)
    print(mename)
    print(newmename)

    if metatype == 'file':
        metatable = 'fileName'
        metable = 'file_name'
        task = "修改文件源名称"
    elif metatype == 'interface':
        metatable = 'interfaceName'
        metable = 'interface_name'
        task = "修改接口源名称"
    elif metatype == 'message':
        metatable = 'messageName'
        metable = 'message_name'
        task = "修改消息源名称"

    us_china = getPinyin(depname)
    db = con(us_china)
    cursor = db.cursor()
    sql = """select {0} from {1} where {2}='{3}';""".format(metable, metatable, metable, newmename)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    update_content = cursor.fetchall()
    if update_content:
        return JsonResponse({'result': 0})
    else:
        sql = """update {0} set {1}='{2}' where {3}='{4}';""".format(metatable, metable, newmename, metable, mename)
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, newmename,
                                                                                               depname,
                                                                                               airTime, endtime, "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        sendlog = str((task,
                       newmename,
                       depname,
                       airTime,
                       endtime,
                       '成功'))
        sendLog = send_log(sendlog)

        return JsonResponse({'result': 1})


# 修改数据源参数
def params_update(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    depname = request.POST.get('depname')  # 部门
    metatype = request.POST.get('metatype')  # 数据元表
    mename = request.POST.get('tableName')
    par_name = request.POST.get('old_fieldname')  # 参数名称
    newpar_name = request.POST.get('field_name')  # 新参数名称
    newpar_desc = request.POST.get('field_desc')  # 新参数描述
    newpar_type = request.POST.get('field_type')  # 新参数类型
    partaname = ''
    metatable = ''
    metaname = ''
    partable = ''
    task = ''
    print(depname)
    print(metatype)
    print(par_name)
    print(newpar_name)
    print(newpar_desc)
    print(newpar_type)

    if metatype == 'file':
        metatable = 'fileName'
        metaname = 'file_name'
        partable = 'fileParams'
        partaname = 'file_name'
        task = "修改文件源参数"
    elif metatype == 'interface':
        metatable = 'interfaceName'
        metaname = 'interface_name'
        partable = 'interfaceParams'
        partaname = 'interface_name'
        task = "修改接口源参数"
    elif metatype == 'message':
        metatable = 'messageName'
        metaname = 'message_name'
        partable = 'messageParams'
        partaname = 'message_name'
        task = "修改消息源参数"

    us_china = getPinyin(depname)
    db = con(us_china)
    cursor = db.cursor()
    # sql = """select {0} from {1} where {2}='{3}';""".format(partaname, partable, partaname, newpar_name)
    # sql_ending = sql.encode(encoding="utf8")
    # cursor.execute(sql_ending)
    # update_content = cursor.fetchall()
    # if update_content:
    #     return JsonResponse({'result': 0})

    sql = """delete from {0} where {1}='{2}';""".format(partable, partaname, par_name)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()

    sql = """select id from {0} where {1}='{2}';""".format(metatable, metaname, mename)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    me_id = cursor.fetchall()[0][0]

    sql = """insert into {0} values (null,'{1}','{2}','{3}','{4}');""".format(partable, newpar_name, newpar_desc, newpar_type, me_id)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, newpar_name, depname,
                                                                                           airTime, endtime, "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   newpar_name,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({'result': 1})


# 删除元数据名称
def del_meta(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    depname = request.POST.get('depname')
    metatype = request.POST.get('metatype')
    mename = request.POST.get('table_en')
    metatable = ''
    metaname = ''
    partable = ''
    paramsid = ''
    me_id = ''
    task = ''
    print(depname)
    print(metatype)
    print(mename)

    if metatype == 'file':
        metatable = 'fileName'
        metaname = 'file_name'
        partable = 'fileParams'
        paramsid = 'filename_id_id'
        task = "删除文件源名称"
    elif metatype == 'interface':
        metatable = 'interfaceName'
        metaname = 'interface_name'
        partable = 'interfaceParams'
        paramsid = 'interface_id_id'
        task = "删除接口源名称"
    elif metatype == 'message':
        metatable = 'messageName'
        metaname = 'message_name'
        partable = 'messageParams'
        paramsid = 'message_id_id'
        task = "删除消息源名称"

    us_china = getPinyin(depname)
    db = con(us_china)
    cursor = db.cursor()
    sql = """select id from {0} where {1}='{2}';""".format(metatable, metaname, mename)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    me_id = cursor.fetchall()[0][0]
    print(me_id,'%%%%')

    # sql = """select {0} from {1} where {2}={3};""".format(metaname, partable, paramsid, me_id)
    # print(sql)
    # sql_ending = sql.encode(encoding="utf8")
    # cursor.execute(sql_ending)
    # pardata = cursor.fetchall()[0]
    # print(pardata,'*************')
    # if pardata:
    sql = """delete from {0} where {1}={2};""".format(partable, paramsid, me_id)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    print('111')

    sql = """delete from {0} where {1}='{2}';""".format(metatable, metaname, mename)
    print(sql, '删除元数据名称')
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, mename, depname,
                                                                                           airTime, endtime, "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   mename,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({'result': 1})


# 删除数据源参数
def del_params(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    depname = request.POST.get('depname')
    metatype = request.POST.get('metatype')
    par_name = request.POST.get('fieldname')
    parname = ''
    partable = ''
    task = ''
    if metatype == 'file':
        partable = 'fileParams'
        parname = 'file_name'
        task = "删除文件源参数"
    elif metatype == 'interface':
        partable = 'interfaceParams'
        parname = 'interface_name'
        task = "删除接口源参数"
    elif metatype == 'message':
        partable = 'messageParams'
        parname = 'message_name'
        task = "删除消息源参数"

    us_china = getPinyin(depname)
    db = con(us_china)
    cursor = db.cursor()
    sql = """delete from {0} where {1}='{2}';""".format(partable, parname, par_name)
    print(sql,'%'*100)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task,par_name,depname,airTime,endtime,"成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   par_name,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({'result': 1})


#  获取字段类型
def get_ftype(request):
    depname = request.POST.get("depname")
    fiename = request.POST.get("fiename")
    print(depname,'库名')
    print(fiename,'字段名')
    depart = getPinyin(depname)
    db = con(depart)
    cursor = db.cursor()
    sql = """select fieldType from add_field where fieldName = '{0}';""".format(fiename)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    ftype = cursor.fetchall()[0][0]
    print(ftype,'字段类型')
    db.commit()
    db.close()

    return JsonResponse({'dbName':depart, 'ftype':ftype})


def serverLogin(request):
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
    # data = {
    #     'userName': "system",
    #     'userPassword': 'oracle',
    #     'userRole':'normal',
    #     'svgVersion':'UNKNOWN',
    #     'browserTimezoneOffset':-480
    # }
    data = {
        'username':'dbadmin',
        'password':'dbadmin@2018',
        'tenantName':''
    }
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    data = json.dumps(data)
    # r = requests.post('https://59.215.191.45:1158/em/console/logon/logon', data=data, verify=False)
    r = requests.post('https://192.168.40.153:4206/resources/server/encryptLogin',data=data,headers=headers, verify=False)
    result = r.text
    return JsonResponse({'result':result})


def oracleLogin(request):
    driver = webdriver.Chrome()
    driver.get("https://192.168.41.3:1158/em/")

    if driver.find_element_by_xpath('//img[@title="登录"]'):
        driver.find_element_by_id('M__Id').send_keys('system')
        driver.find_element_by_id('M__Ida').send_keys('oracle')
        driver.find_element_by_id('M__Idb').send_keys('Normal')
        driver.find_element_by_xpath('//img[@title="登录"]').click()
        return JsonResponse({"result":1})



def ogCodeURl(request):
    if request.method == "GET":
        ogCode = request.GET.get("ogCode")
        db = con("test")
        cursor = db.cursor()
        sql = """select ogCode from department;"""
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()
        ogcode = cursor.fetchall()
        # print(ogcode)
        for forone in ogcode:
            for fortwo in forone:
                # print(fortwo)
                if ogCode in fortwo:
                    db = con("test")
                    cursor = db.cursor()
                    sql = """select hosts,us_dataname from department where ogCode='{0}';""".format(ogCode)
                    sql_ending = sql.encode(encoding="utf8")
                    cursor.execute(sql_ending)
                    db.commit()
                    db.close()
                    host_dataname = cursor.fetchall()
                    for forone in host_dataname:
                        host=forone[0]
                        dataname = forone[1]
                        key = ""
                        url = "http://59.215.191.43:8000/departAdmin/{0}/{1}".format(host,dataname)
                        dict1 = {"key":key, "url": url}
                        result = str(dict1)
                        return HttpResponse(result, content_type='application/json; charset=utf-8')
                else:
                    pass


def content(request):
    import pymysql
    import xml
    fileName=''
    fileUrl=''
    hodts=''
    db = pymysql.connect('127.0.0.1',
                         'root',
                         'root',
                         'test',
                         charset='utf8')

    cursor = db.cursor()
    sql = """select hosts from department where ogCode = '{0}';""".format("1b1c5a4d-ebb7-44a5-bf89-cb26ae7e0d1d")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    hosts = cursor.fetchall()[0][0]
    db.commit()
    db.close()
    print(hosts)
    print("部门获取成功")
    db = pymysql.connect('192.168.41.92',
                             'dispatchSys',
                             'DispatchSys',
                             'datamarket',
                             charset='utf8')
    cursor = db.cursor()
    sql = """select name,oss_url from dm_file where id={0};""".format(151)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    fileName_url = cursor.fetchall()
    db.commit()
    db.close()
    for forone in fileName_url:
        fileName = forone[0]
        fileUrl = forone[1]


    xml_obj = xml.dom.minidom.parse('./url_config/add_server.xml')
    root = xml_obj.documentElement
    url = root.getElementsByTagName('url')[0].firstChild.data
    method = root.getElementsByTagName('requests')[0].firstChild.data
    data = {"serviceName":fileName,
            "hosts": hosts,
            "uris": "/rsb/zyzgzs/file/test/test",
            "upstream_url": fileUrl
            }
    print(data)
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
    url="http:/"+hodts+'/rsb/zyzgzs/file/test/test'
    dict1 = {"apikey": "", "url":url}
    result = str(dict1)
    return HttpResponse(result, content_type='application/json; charset=utf-8')


def haiyunDatalink(request):
    if request.method == "POST":
        apikey=""
        isflag = True
        sqlIp=""
        depart = ''
        visitCount = request.POST.get('visitCount')
        columns = request.POST.get('columns')
        resourceName = request.POST.get('resourceName')
        processId = request.POST.get('processId')
        resourceId = request.POST.get('resourceId')
        ogCode = request.POST.get('ogCode')
        tableName = request.POST.get('tableName')
        datapath_id = request.POST.get('datapath_id')
        detail=request.POST.get('detail')
        intResourceId=int(resourceId)

        #parameter=str({
        #    "visitCount":visitCount,
        #    "columns":columns,
        #    "processId":processId,
        #    "resourceId":resourceId,
        #    "ogCode":ogCode,
        #    "tableName":tableName,
        #    "detail":detail,
        #    "type":paramstype
        #})
        typeNumber=0
        db = pymysql.connect('192.168.41.92',
                             'dispatchSys',
                             'DispatchSys',
                             'datamarket',
                             charset='utf8')
        cursor = db.cursor()
        sql = """select datatype from dm_data where id ={0};""".format(resourceId)
        typeNumber = 0
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()
        setType = cursor.fetchall()
        for one in setType:
            for Type in one:
                typeNumber = Type
        print(typeNumber)
        #parameter = pymysql.escape_string(parameter)
        if typeNumber == 1:
            fileName = ''
            fileUrl = ''
            hosts = ''
            #获取部门
            print("获取部门开始")
            db = pymysql.connect('127.0.0.1',
                                 'root',
                                 'root',
                                 'test',
                                 charset='utf8')

            cursor = db.cursor()
            sql = """select hosts from department where ogCode = '{0}';""".format(ogCode)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            hosts = cursor.fetchall()[0][0]
            db.commit()
            db.close()
            print(hosts)
            print("部门获取成功")

            db = pymysql.connect('192.168.41.92',
                                 'dispatchSys',
                                 'DispatchSys',
                                 'datamarket',
                                 charset='utf8')
            cursor = db.cursor()
            sql = """select name,oss_url from dm_file where id={0};""".format(datapath_id)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            fileName_url = cursor.fetchall()
            db.commit()
            db.close()
            for forone in fileName_url:
                fileName = forone[0]
                fileUrl = forone[1]

            xml_obj = xml.dom.minidom.parse('./url_config/add_server.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            data = {"serviceName": fileName,
                    "hosts": hosts,
                    "uris": "/rsb/zyzgzs/file/test/test",
                    "upstream_url": fileUrl
                    }
            print(data)
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

            url = "http:/" + hosts + '/rsb/zyzgzs/file/test/test'
            dict1 = {"apikey": "", "url": url}
            result = str(dict1)
            return HttpResponse(result, content_type='application/json; charset=utf-8')

        elif typeNumber == 2:

            interfaceUrl = ""
            interfaceName = ''
            hosts = ''

            #获取部门
            print("获取部门")
            db = pymysql.connect('127.0.0.1',
                                 'root',
                                 'root',
                                 'test',
                                 charset='utf8')

            cursor = db.cursor()
            sql = """select hosts from department where ogCode = '{0}';""".format(ogCode)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            hosts = cursor.fetchall()[0][0]
            db.commit()
            db.close()
            print(hosts)
            print("部门获取成功")


            db = pymysql.connect('192.168.41.92',
                                 'dispatchSys',
                                 'DispatchSys',
                                 'datamarket',
                                 charset='utf8')
            cursor = db.cursor()
            sql = """select description,address from dm_interface where id={0};""".format(datapath_id)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            fileName_url = cursor.fetchall()
            db.commit()
            db.close()
            for forone in fileName_url:
                interfaceName = forone[0]
                interfaceUrl = forone[1]
                if interfaceName != "":
                    pettern = re.compile(r"<p>(.*?)</p>")
                    interfaceName = re.findall(pettern, interfaceName)[0]
                else:
                    interfaceName = "tongyongshuju"

            xml_obj = xml.dom.minidom.parse('./url_config/add_server.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            data = {"serviceName": interfaceName,
                    "hosts": hosts,
                    "uris": "/rsb/zyzgzs/interface/test/test",
                    "upstream_url": interfaceUrl
                    }
            print(data)
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

            url = "http:/" + hosts + '/rsb/zyzgzs/interface/test/test'
            dict1 = {"apikey": "", "url": url}
            result = str(dict1)
            return HttpResponse(result, content_type='application/json; charset=utf-8')

        elif typeNumber == 8:

            # 获取部门
            print("获取部门")
            db = pymysql.connect('127.0.0.1',
                                 'root',
                                 'root',
                                 'test',
                                 charset='utf8')

            cursor = db.cursor()
            sql = """select hosts from department where ogCode = '{0}';""".format(ogCode)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            hosts = cursor.fetchall()[0]
            hosts = hosts[0]
            #for forone in hosts:
            #    hosts=forone[0]
            db.commit()
            db.close()
            print(hosts)
            print("部门获取成功")

            xml_obj = xml.dom.minidom.parse('./url_config/add_username.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            params = {"username": processId}
            try:
                res = requests.request(method=method,
                                       url=url,
                                       data=params,
                                       timeout=0.5)
            except requests.exceptions.ConnectionError:
                xml_obj = xml.dom.minidom.parse('./url_config/req_apikey.xml')
                root = xml_obj.documentElement
                url = root.getElementsByTagName('url')[0].firstChild.data
                method = root.getElementsByTagName('requests')[0].firstChild.data
                params = {"username": processId}
                res = requests.request(method=method,
                                       url=url,
                                       params=params)
                res_dict = json.loads(res.text)
                apikey = res_dict["result"]
            except requests.exceptions.ReadTimeout:
                xml_obj = xml.dom.minidom.parse('./url_config/req_apikey.xml')
                root = xml_obj.documentElement
                url = root.getElementsByTagName('url')[0].firstChild.data
                method = root.getElementsByTagName('requests')[0].firstChild.data
                params = {"username": processId}
                res = requests.request(method=method,
                                       url=url,
                                       params=params)
                res_dict = json.loads(res.text)
                apikey = res_dict["result"]

            print("添加组")
            xml_obj = xml.dom.minidom.parse('./url_config/add_group.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            params = {"group": processId,
                      "username": processId,
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

            print("添加组成功")
            i = 0
            with open("./sql_file/count.txt", "r") as f:
                strcount = f.read()
                i = int(strcount)

            sqlIp = 'http://1.255.1.202:3000/api/db?id={0}'.format(i)
            # sqlIp = 'http://1.255.1.202:3000/api/db?id={0}'.format(str(i))
            print(type(columns))
            print(columns)
            listcolumns = eval(columns)
            print(type(listcolumns))
            tableName1 = "FRK_LIB_SCHEMAS."+tableName
            print(listcolumns)
            # briName = "table." + ".".join(str(i) for i in listcolumns) + processId
            field = "$".join(str(i) for i in listcolumns)
            #sql_yuju = "select {0} from {1};".format(field, tableName)
            #leng = len(listcolumns)
            #pinjielist = []
            #for k in range(leng):
            #    if k == leng - 1:
            #        a = listcolumns[k] + "=" + '\"%s"'
            #    else:
            #        a = listcolumns[k] + "=" + '\"%s"' + " " + "and" + " "
            #    pinjielist.append(a)
            #table = "FRk_LIB_SCHEMAS."+ tableName
            #sql = "select * from {0} where".format(table) + " " + "".join(pinjielist) + ";"
            sql = "select {0} from {1};".format(field, tableName1)
            print(sql)

            with open("./sql_file/db.search.sql", "a+") as f:
                f.write(sql + "\n")
            strI = str(i + 1)
            with open("./sql_file/count.txt", "w") as f:
                f.write(strI)
            #with open("./sql_file/test.sql", "a+") as f:
            #    f.write(sql + "\n")
            print(11111111)
            print(detail)

            detailfile="桥接名称："+ detail +"  "+"数据区："+"大数据"+"  "+"sql语句："+sql
            with open("./sql_file/db.detail.sql", "a+") as f:
                f.write(detailfile+"\n")
            uspinyin = getPinyin(detail)
            print(detailfile)
            uris = '/qyxyk/gsj/db/'+uspinyin+"/"+uspinyin
            print(1)
            xml_obj = xml.dom.minidom.parse('./url_config/add_server.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            data = {"serviceName": detail,
                    "hosts": hosts,
                    "uris": uris,
                    "upstream_url": sqlIp
                    }
            print(data)
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

            time.sleep(15)
            print("添加流控")
            name="rate-limiting"
            xml_obj = xml.dom.minidom.parse('./url_config/add_control.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            # consumer_id = request.session.get("consumer_id")
            # consumer_id = "11cd88d2-3e6a-464f-8dc3-5c1a42e8c54b"
            params = {"name": name,
                      "day": visitCount,
                      "serviceName": detail,
                      "username": processId,
                      }
            try:
                res = requests.request(method=method,
                                       url=url,
                                       data=params,
                                       timeout=0.5)
                task = "添加流量控制"
            except requests.exceptions.ConnectionError:
                isTrue = False
                task = "添加流量控制"
            except requests.exceptions.ReadTimeout:
                isTrue = False
                task = "添加流量控制"
            print("添加流控成功")

            print("添加访问控制开始")
            aclName = 'acl'
            xml_obj = xml.dom.minidom.parse('./url_config/add_acl.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            params = {"serviceName": detail,
                      "name": aclName,
                      "whitelist": processId
                      }
            print(url, method, params, '*' * 100)
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

            print("添加访问控制成功")

            uspinyin = getPinyin(detail)
            url = "http:/" + hosts + '/qyxyk/gsj/db/'+uspinyin+"/"+uspinyin
            dict1 = {"apikey": apikey, "url": url}
            result = str(dict1)
            #db = pymysql.connect('192.168.41.92',
	    #				 'dispatchSys',
	    #				 'DispatchSys',
	    #				 'datamarket',
	    #				 charset='utf8')
            #cursor = db.cursor()
            #sql = """insert into dm_interface (original_address,createtime,updatetime,newaddress) values('abcd','2018-10-19 00:00:00','2018-10-19 00:00:00','{0}');""".format("wdawda")
            #sql_ending = sql.encode(encoding="utf8")
            #cursor.execute(sql_ending)
            #fileName_url = cursor.fetchall()
            #db.commit()
            #db.close()
            #print(parameter)
            nowtime = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            db = pymysql.connect('192.168.41.92',
                                 'dispatchSys',
                                 'DispatchSys',
                                 'datamarket',
                                 charset='utf8')
            cursor = db.cursor()
            # sql = """select description,address from dm_interface where id={0};""".format(datapath_id)
            #sql = """insert into dm_interface (original_address,parameter,description,createtime,updatetime,dmlflag,isauthorize,serviceType,errorCodes,methods,department,resource_id,newaddress) values('{0}','{1}','{2}','{3}','{4}',{5},{6},'{7}','{8}','{9}','{10}',{11},'{12}');""".format(sqlIp,parameter,detail,nowtime,nowtime,0,0,"http","200","POST",ogCode,resourceId,url)
            print(sql)
            sql = """insert into dm_interface (original_address,createtime,updatetime,resource_id,newaddress) values('{0}','{1}','{2}','{3}','{4}');""".format(
                "无", nowtime, nowtime, intResourceId, url)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            db.commit()
            db.close()

            return HttpResponse(result, content_type='application/json; charset=utf-8')


def get_departs(request):
    depart_list = []
    db = con("test")
    cursor = db.cursor()
    sql1 = """select dataname from department; """
    # sql1 = """select * from mylog;"""
    sql_ending = sql1.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_sql = cursor.fetchall()
    print(set_sql)
    for i in set_sql:
        # print(i[0])
        depart_list.append(i[0])
    db.close()
    return JsonResponse({'result':depart_list})


# 获取首页总览信息
def get_cataloginfo(request):
    cataloginfo_list = []
    departname_list = []
    db = con("test")
    cursor = db.cursor()
    sql = """select dataname from department;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    departname = cursor.fetchall()
    for depart in departname:
        print(depart[0], '部门名称')
        departname_list.append(depart)
    db.close()
    for depname in departname_list:
        us_depName = getPinyin(depname[0])

        # 获取用户数量
        db = con("test")
        cursor = db.cursor()
        # 获取数据目录数量
        sql = """select count(*) from Uuser where depart='{0}';""".format(us_depName)
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        user_count = cursor.fetchall()[0][0]
        print(depname[0], user_count, '--用户目录数量')
        # 获取部门总数
        sql = """select count(*) from department;""".format(us_depName)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        depart_count = cursor.fetchall()[0][0]
        print(depname[0], depart_count, '--用户目录数量')
        db.close()

        db = con(us_depName)
        cursor = db.cursor()
        # 获取数据目录数量
        sql = """select count(*) from Uservice;"""
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        service_count = cursor.fetchall()[0][0]
        print(depname[0], service_count, '--数据目录数量')

        # 获取安全目录数量
        sql = """select count(*) from Uacl;"""
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        acl_count = cursor.fetchall()[0][0]

        sql = """select count(*) from Ucontrols;"""
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        controls_count = cursor.fetchall()[0][0]
        safe_count = acl_count + controls_count
        print(depname[0], safe_count, '--安全目录数量')

        # 获取数据桥接数量
        sql = """select count(*) from dbList;"""
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        dblist_count = cursor.fetchall()[0][0]

        sql = """select count(*) from fileList;"""
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        filelist_count = cursor.fetchall()[0][0]

        sql = """select count(*) from interfaceList;"""
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        interfacelist_count = cursor.fetchall()[0][0]

        sql = """select count(*) from messageList;"""
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        messagelist_count = cursor.fetchall()[0][0]
        bridging_count = dblist_count + filelist_count + interfacelist_count + messagelist_count
        print(depname[0], bridging_count, '--数据桥接数量')
        db.close()

        cataloginfo_list.append([depname[0], user_count, service_count, safe_count, bridging_count, depart_count])
    print(cataloginfo_list, '--总览信息')

    return JsonResponse({'result': cataloginfo_list})


# 接口
# 中软通知接口
# def getNotice(request):
#     airTime = time.time()
#     timeArray = time.localtime(airTime)
#     airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
#     print("通知接口")
#     if request.method == "POST":
#         resourceId = request.POST.get('resourceId')
#         type = request.POST.get('type')
#         print(resourceId, "resourceId")
#         print(type, 'type')
#         db = con("test")
#         cursor = db.cursor()
#         sql = """insert into noticedata values (null,'{0}','{1}','{2}',{3});""".format(airTime, resourceId, type, 1)
#         print(sql)
#         sql_ending = sql.encode(encoding="utf8")
#         cursor.execute(sql_ending)
#         db.commit()
#         db.close()
#
#         if resourceId:
#             result = 1
#         else:
#             result = 0
#     return JsonResponse({'result': result})

def getNotice(request):
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print("通知接口")
    # 中软数据库查询一、二、三级目录,ogcode
    # 部门初始化
    us_dartment = ""
    # 组织机构代码
    ogCode = ""
    # 数据目录
    three = ""
    # 一级目录
    first = ""
    # 二级目录
    second = ""
    # 未处理一级id
    oneid = ""
    # 未处理三级id
    twoid = ""
    # 数据库
    database = ""
    # 处理完一级目录id
    firstId = ""
    # 处理完二级目录id
    secondid = ""
    # 数据目录名称
    data_name = ""
    if request.method == "POST":
        resourceId = request.POST.get('resourceId')
        type = request.POST.get('type')
        print(resourceId, "resourceId")
        print(type, 'type')
        db = con("test")
        cursor = db.cursor()
        sql = """insert into noticedata values (null,'{0}','{1}','{2}',{3});""".format(airTime, resourceId, type, 1)
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        db = pymysql.connect('59.215.191.18',
                             'dispatchGLA',
                             'DispatchGLA',
                             'datamarket',
                             charset='utf8')
        cursor = db.cursor()
        print('连接中间库')
        # 海云查询
        sql = """SELECT 
            `g`.`org_no` AS `ogcode`,  -- 部门组织代码
            t.`name` data_name,  -- 数据名称
            sd.`name` child_dir_name,  -- 子目录名称
            sdd.`name` root_name --  根目录名称
        FROM dm_dataset ds LEFT JOIN dm_data t    ON t.`dataset_id`=ds.`id`
        LEFT JOIN dm_data_directory dd         ON dd.`data_id` =t.`id`
        LEFT JOIN dm_share_sub_directory sd     ON dd.`share_sub_directory_id`=sd.`id`
        LEFT JOIN dm_share_data_directory sdd    ON dd.`share_data_directory_id`=sdd.`id`
    LEFT JOIN dm_industry      industry         ON industry .`id`=sd.`industry_id`
    LEFT JOIN `datamarket`.`dm_group` `g`  ON `ds`.`group_id` = `g`.`id`
    WHERE ds.`status`=4
    AND sdd.`status`=4
    AND sd.id IS NOT NULL
    and t.id={0};""".format(resourceId)
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        xinxi = cursor.fetchall()
        print(xinxi)
        db.commit()
        db.close()
        for one in xinxi:
            ogCode = one[0]
            first = one[3]
            second = one[2]
            three = one[1]
        print(ogCode, first, second, three)
        # 判断是否存在部门
        db = con('test')
        cursor = db.cursor()
        sql = """select us_dataname from department where ogCode = '{0}';""".format(ogCode)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        us_dartment = cursor.fetchall()
        db.commit()
        db.close()
        print()
        if us_dartment:
            database = us_dartment[0][0]
            print(database)
            # 判断是否存在一级目录
            db = con(database)
            cursor = db.cursor()
            sql = """select id from AdminFirst where chinese_abb = '{0}';""".format(first)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            oneid = cursor.fetchall()
            db.commit()
            db.close()
            if oneid:
                firstId = oneid[0][0]
                print(firstId)
                # 判断是否存在二级目录
                db = con(database)
                cursor = db.cursor()
                sql = """select id from AdminSecond where chinese_abb = '{0}';""".format(second)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                twoid = cursor.fetchall()
                db.commit()
                db.close()
                print(twoid)
                if twoid:
                    secondid = twoid[0][0]
                    db = con(database)
                    cursor = db.cursor()
                    sql = """select chinese_abb from AdminThird where chinese_abb = '{0}';""".format(three)
                    sql_ending = sql.encode(encoding="utf8")
                    cursor.execute(sql_ending)
                    dataName = cursor.fetchall()
                    db.commit()
                    db.close()
                    # 判断是否存在数据名称
                    if dataName:
                        # 该数据已经添加无需插入
                        result = '{"code":0,"status":"该服务目录已经存在"}'

                        return HttpResponse(result, content_type='application/json; charset=utf-8')
                    else:
                        # 一级，二级目录都有，无数据名称可以插入
                        data_name = getPinyin(three)
                        db = con(database)
                        cursor = db.cursor()
                        sql = """INSERT into AdminThird VALUES (null,'{0}','{1}',0,{2},{3});""".format(
                            data_name, three, firstId, secondid)
                        sql_ending = sql.encode(encoding="utf8")
                        cursor.execute(sql_ending)
                        db.commit()
                        db.close()
                        result = '{"code":0,"status":"成功"}'

                        return HttpResponse(result, content_type='application/json; charset=utf-8')
                else:
                    print(2222222)
                    # 向二级目录插入二级目录
                    twoCatalog = getPinyin(second)
                    print(twoCatalog)
                    db = con(database)
                    cursor = db.cursor()
                    sql = """INSERT into AdminSecond VALUES (null,'{0}','{1}',0,{2})""".format(twoCatalog, second, firstId)
                    sql_ending = sql.encode(encoding="utf8")
                    cursor.execute(sql_ending)
                    db.commit()
                    db.close()
                    # 查询刚刚插入二级目录的id
                    db = con(database)
                    cursor = db.cursor()
                    sql = """select id from AdminSecond where chinese_abb = '{0}';""".format(second)
                    sql_ending = sql.encode(encoding="utf8")
                    cursor.execute(sql_ending)
                    twoid = cursor.fetchall()
                    db.commit()
                    db.close()
                    secondid = twoid[0][0]

                    # 将一级目录，二级目录id取出插入三级目录中
                    print(secondid)
                    data_name = getPinyin(three)
                    db = con(database)
                    cursor = db.cursor()
                    sql = """INSERT into AdminThird VALUES (null,'{0}','{1}',0,{2},{3});""".format(data_name, firstId, secondid)
                    sql_ending = sql.encode(encoding="utf8")
                    cursor.execute(sql_ending)
                    db.commit()
                    db.close()
                    result = '{"code":0,"status":"成功"}'
                    return HttpResponse(result, content_type='application/json; charset=utf-8')

            else:
                # 插入一级目录
                print(first)
                oneCatalog = getPinyin(first)
                print(oneCatalog)
                db = con(database)
                cursor = db.cursor()
                sql = """INSERT into AdminFirst VALUES (null,'{0}','{1}',0);""".format(oneCatalog, first)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                twoid = cursor.fetchall()
                db.commit()
                db.close()
                # 获取一级目录的id
                db = con(database)
                cursor = db.cursor()
                sql = """select id from AdminFirst where chinese_abb = '{0}';""".format(first)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                oneid = cursor.fetchall()
                db.commit()
                db.close()

                firstId = oneid[0][0]
                print(firstId)
                # 向二级目录插入二级目录
                twoCatalog = getPinyin(second)
                print(twoCatalog)
                db = con(database)
                cursor = db.cursor()
                sql = """INSERT into AdminSecond VALUES (null,'{0}','{1}',0,{2})""".format(twoCatalog, second, firstId)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                db.commit()
                db.close()
                print('二级目录插入成功')
                # 查询刚刚插入二级目录的id
                db = con(database)
                cursor = db.cursor()
                sql = """select id from AdminSecond where chinese_abb = '{0}';""".format(second)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                twoid = cursor.fetchall()
                db.commit()
                db.close()
                secondid = twoid[0][0]
                print(secondid)
                data_name = getPinyin(three)
                print(data_name)
                db = con(database)
                cursor = db.cursor()
                sql = """INSERT into AdminThird VALUES (null,'{0}','{1}',0,{2},{3});""".format(data_name, three, firstId, secondid)
                print(sql)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                db.commit()
                db.close()
                result = '{"code":0,"status":"成功"}'

                return HttpResponse(result, content_type='application/json; charset=utf-8')
        else:
            result = '{"code":0,"status":"该部门没有添加"}'

            return HttpResponse(result, content_type='application/json; charset=utf-8')


# 获取数据上架平台访问地址接口
def getDatalinkUrls(request):
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print(airTime, '时间')
    # 数据上架平台访问地址
    datalink_url = ''
    depUrl = ''
    if request.method == "POST":
        # 组织机构代码
        org_code = request.POST.get('org_code')
        print(org_code, 'org_code')
        # 判断url类型（1、用户管理页面 2、管理页面 3、超级管理页面）
        url_type = request.POST.get('url_type')
        print(url_type, type(url_type), 'url_type')
        db = con("test")
        cursor = db.cursor()
        sql = """select us_dataname,hosts,dataname from department where ogCode='{0}';""".format(org_code)
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        depart_url = cursor.fetchall()
        print(depart_url, '部门名称，映射域名')
        db.close()
        if depart_url:
            if url_type == '1':
                depUrl = '用户'
                datalink_url = 'http://59.215.191.43:8000/commonUser/{0}/{1}/'.format(depart_url[0][1], depart_url[0][0])
            elif url_type == '2':
                depUrl = '管理'
                datalink_url = 'http://59.215.191.43:8000/departAdmin/{0}/{1}/'.format(depart_url[0][1], depart_url[0][0])
            elif url_type == '3':
                depUrl = '超级管理'
                datalink_url = 'http://59.215.191.43:8000/admin/'
            else:
                depUrl = False
                datalink_url = 'Error:urlType error！ Tips：1、User Management Page 2、Management Page 3、Super Management Page'
        else:
            depUrl = False
            datalink_url = 'Error:Department not added！'
        print(datalink_url)
        if depUrl :
            # 获取记录存储
            db = con("test")
            cursor = db.cursor()
            sql = """insert into getDatalinkUrls values (null,'{0}','{1}','{2}','{3}')""".format(airTime, depart_url[0][2],
                                                                                                 depUrl, datalink_url)
            print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            db.commit()
            db.close()

    return JsonResponse({'datalink_url': datalink_url})


#  海云入参
def AchieveParticipation(request):
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    # 用户ID
    procId = ''
    apikey = ''
    depart_name = ''
    data_name = ''
    name = 'rate-limiting'
    visitAverageCall = ''
    istransact = 0
    us_china = ''
    if request.method == "POST":
        # 资源ID
        resourceId = request.POST.get('resourceId')
        print(resourceId, '资源ID')
        # 流程ID，用于对应apiKey的唯一性
        procId = request.POST.get('procId')
        print(procId, '用户ID')
        # 用户勾选的字段
        columns = request.POST.get('columns')
        # 每年访问次数
        visitAverageCall = request.POST.get('visitAverageCall')
        print(visitAverageCall, '每年访问次数')
        # 海云入参生成数据目录

        # 适用范围，x天
        visitUseDays = request.POST.get('visitUseDays')
        # 入参放入文档
        with open("./file/controlparameter.txt", "a+") as f:
            f.write("resourceId:" + resourceId + "procId:" + procId + "\n")

        db = middle_con("datamarket")
        cursor = db.cursor()
        sql = """select depart_name,data_name from interface_description where resource_id='{0}';""".format(resourceId)
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        interfacedesc = cursor.fetchall()
        print(interfacedesc, '中间库返回结果')
        if interfacedesc:
            depart_name = interfacedesc[0][0]
            print(depart_name, '部门名称')
            data_name = interfacedesc[0][1]
            print(data_name, '数据目录名称')
            db.close()
            print(interfacedesc, "中间库返回信息")
            us_china = getPinyin(depart_name)
            db = con("test")
            cursor = db.cursor()
            sql = """select username from Uuser where username='{0}';""".format(procId)
            print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            user_name = cursor.fetchall()
            print(user_name, '用户')
            # 判断用户是否存在
            if user_name:
                print("获取apikey")
                # 获取apikey
                apikey = get_apikey(procId)
                print(apikey,'apikey')
            else:
                # 添加用户
                print('添加用户')
                xml_obj = xml.dom.minidom.parse('./url_config/add_username.xml')
                root = xml_obj.documentElement
                url = root.getElementsByTagName('url')[0].firstChild.data
                method = root.getElementsByTagName('requests')[0].firstChild.data
                params = {"username": procId}
                try:
                    res = requests.request(method=method,
                                           url=url,
                                           data=params,
                                           timeout=0.5)
                except requests.exceptions.ConnectionError:
                    xml_obj = xml.dom.minidom.parse('./url_config/req_apikey.xml')
                    root = xml_obj.documentElement
                    url = root.getElementsByTagName('url')[0].firstChild.data
                    method = root.getElementsByTagName('requests')[0].firstChild.data
                    params = {"username": procId}
                    res = requests.request(method=method,
                                           url=url,
                                           params=params)
                    res_dict = json.loads(res.text)
                    apikey = res_dict["result"]
                except requests.exceptions.ReadTimeout:
                    xml_obj = xml.dom.minidom.parse('./url_config/req_apikey.xml')
                    root = xml_obj.documentElement
                    url = root.getElementsByTagName('url')[0].firstChild.data
                    method = root.getElementsByTagName('requests')[0].firstChild.data
                    params = {"username": procId}
                    res = requests.request(method=method,
                                           url=url,
                                           params=params)
                    res_dict = json.loads(res.text)
                    apikey = res_dict["result"]

                sql = """insert into Uuser values (null,'{0}','{1}','{2}');""".format(procId, apikey, us_china)
                sql_ending = sql.encode(encoding="utf8")
                cursor.execute(sql_ending)
                db.commit()
                db.close()
                #   添加安全目录数据用户
                obj = user.objects.create(id=None,
                                          username=procId,
                                          api_key=apikey,
                                          )
                obj.save(using='Safe_dic')
            # 增加流量控制
            print("增加流控")
            db = con(us_china)
            cursor = db.cursor()
            sql = """insert into Ucontrols (controlsName, userName, consumer_id,serviceName,day)values ('{0}','{1}','{2}','{3}','{4}');""".format(name,
                                                                                                procId,
                                                                                                "f3381508-fc55-4ddb-98d2-4f63304389d7",
                                                                                                data_name,
                                                                                                visitAverageCall
                                                                                                )
            print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            db.commit()
            db.close()
            print("添加安全流控")
            # 添加安全目录流量控制
            obj = FlowControl.objects.create(
                name=name,
                username=procId,
                serviceName=data_name,
                user_day=visitAverageCall,
            )
            obj.save(using='Safe_dic')
            print("添加流控到安全目录")
            xml_obj = xml.dom.minidom.parse('./url_config/add_control.xml')
            root = xml_obj.documentElement
            url = root.getElementsByTagName('url')[0].firstChild.data
            method = root.getElementsByTagName('requests')[0].firstChild.data
            # consumer_id = request.session.get("consumer_id")
            # consumer_id = "11cd88d2-3e6a-464f-8dc3-5c1a42e8c54b"
            params = {"name": name,
                      "day": visitAverageCall,
                      "serviceName": data_name,
                      "username": procId,
                      }
            try:
                res = requests.request(method=method,
                                       url=url,
                                       data=params,
                                       timeout=0.5)
            except requests.exceptions.ConnectionError:
                istransact = 0
                print(istransact)
                result = {"procId": procId, "code": "0", "apiKey": apikey}

            except requests.exceptions.ReadTimeout:
                istransact = 0
                print(istransact)
                result = {"procId": procId, "code": "0", "apiKey": apikey}

        else:
            istransact = 1
            print(istransact)
            result = {"procId": procId, "code": "1", "apiKey": None}
        # 海云获取apikey信息存储
        db = con("test")
        cursor = db.cursor()
        sql = """insert into hyParticipation (airTime,procId,resourceId,visitAverageCall,isTransact) values ('{0}','{1}','{2}','{3}',{4});""".format(airTime, procId,
                                                                                                  resourceId,
                                                                                                  visitAverageCall,
                                                                                                  istransact )
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

    return JsonResponse( result )


#点击侧边栏跳转到指定部门信息栏中
def depart_classify(request):
    Countrylist = []
    countList = []
    #获取所需的分类类型，1：国家部委 2：省直属部门 3：地州市
    # 国家部委
    ClassifyType = request.POST.get("type")
    if  ClassifyType == "1":
        db = con('test')
        cursor = db.cursor()
        sql = """select dataname from department where dataname like "%国家%";"""
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        city_name = cursor.fetchall()
        for i in city_name:
            Countrylist.append(i[0])
        for cityName in Countrylist:
            encityName = getPinyin(cityName)
            CatalogCount = get_num(encityName)
            countList.append(CatalogCount)
        db.close()
        # print(countList,11111111111111111111111111111111)
        return JsonResponse({'result':countList})

    # 省直属部门
    elif ClassifyType == "2":
        db = con('test')
        cursor = db.cursor()
        sql = """select dataname from department where dataname like "%贵州省%" and  dataname  not  like "%市" and dataname not like "%州";
"""
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        country_name = cursor.fetchall()
        # print(country_name,'--省直属部门')
        for i in country_name:
            Countrylist.append(i[0])
        for con_name in Countrylist:
            encon_name = getPinyin(con_name)
            CatalogCount = get_num(encon_name)
            countList.append(CatalogCount)
        db.close()
        # print(countList,22222222222222222222222222222222222)
        return JsonResponse({'result': countList})
    # 地州市
    elif ClassifyType == "3":
        db = con('test')
        cursor = db.cursor()
        sql = """select dataname from department where dataname like '%市' or dataname like '%州';"""
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        Village_name = cursor.fetchall()
        for i in Village_name:
            Countrylist.append(i[0])
        for VillageName in Countrylist:
            envillagename = getPinyin(VillageName)
            CatalogCount = get_num(envillagename)
            countList.append(CatalogCount)
        db.close()
        # print(countList,333333333333333333333333)
        return JsonResponse({'result':countList})
    # 省外部门
    else:
        db = con('test')
        cursor = db.cursor()
        sql = """select dataname from department where dataname  not like'%贵州省%' and dataname not like '%国家%';"""
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        outcity = cursor.fetchall()
        for i in outcity:
            Countrylist.append(i[0])
        for outcityName in Countrylist:
            enoutcityname = getPinyin(outcityName)
            CatalogCount = get_num(enoutcityname)
            countList.append(CatalogCount)
        db.close()
        # print(countList,333333333333333333333333)
        return JsonResponse({'result':countList})


def get_departInfo(requests):
    db = con('test')
    cursor = db.cursor()
    sql = """select count(dataname) from department where dataname like "%国家%";"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    country = cursor.fetchall()[0][0]
    sql = """select count(dataname) from department where dataname like "%州" or dataname like "%市";"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    city = cursor.fetchall()[0][0]
    sql = """select count(dataname) from department where dataname like "%贵州省%" and  dataname  not  like "%市" and dataname not like "%州";"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    village = cursor.fetchall()[0][0] 
    sql = """select count(dataname) from department where dataname  not like'%贵州省%' and dataname not like '%国家%';"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    outcity = cursor.fetchall()[0][0]
    dict_catalog = {'country':country, 'city':city, 'village':village,'outcity':outcity}
    # print(dict_catalog,111111111111111111111111111111)
    return JsonResponse({'result':dict_catalog})


# 元数据同步（表、字段结构）
def metadata_synchro(request):
    result = 1
    # 获取部门名称
    department = request.POST.get('department')
    print(department,'部门名称')
    us_depart = getPinyin(department)
    # 连接本地库，获取用户名
    db = con('test')
    cursor = db.cursor()
    # 获取用户名
    sql = """select metadata_user from dm_group where group_name = '{0}';""".format(department)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    metauser = cursor.fetchall()[0][0]
    print(metauser,'用户名')
    db.close()

    # 数据区传参，获取相应元数据（表、字段）结构信息
    # 请求头
    headers = {
        "content-type": "application/json"
    }
    # 请求参数
    data = {
        "id": "700cff2e0582faad78dd1c3314dcab5b",
        "params": ["{0}".format(metauser)],
        "paramsnum": 1
    }
    datajson = json.dumps(data)
    print(data)
    try:
        html = requests.request(method="POST", url="http://1.255.1.150:3003/api/db?id=19", headers=headers,data=datajson)
        # 获取到的数据区元数据（表、字段）结构
        metadata = html.text
        metadata = eval(metadata)
        MetaData = metadata.get("result")
        print(MetaData,'数据区返回结果')
        # 数据清洗
        if MetaData:
            db = con(us_depart)
            cursor = db.cursor()
            print("清空元数据信息")
            # 清空字段结构信息
            sql = """delete from add_field;"""
            print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            db.commit()
            # 清空表结构信息
            sql = """delete from  savetable;"""
            print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            db.commit()
            for meta_data in MetaData:
                # 用户名
                GRANTEE_NAME = meta_data.get("GRANTEE_NAME")
                # schema名字|库名
                SCHEMA_NAME = meta_data.get("SCHEMA_NAME")
                # 表名
                OBJECT_NAME = meta_data.get("OBJECT_NAME")
                # 字段名
                COLUMN_NAME = meta_data.get("COLUMN_NAME")
                # 字段类型
                SQL_DATA_TYPE = meta_data.get("SQL_DATA_TYPE")
                # 字段长度
                COLUMN_SIZE = meta_data.get("COLUMN_SIZE")
                # 字段描述
                TEXT = meta_data.get("TEXT")
                # 表描述
                TABLE_TEXT = meta_data.get("TABLE_TEXT")
                DATA_TYPE_SIZE = SQL_DATA_TYPE + "(" + COLUMN_SIZE + ")"
                print(GRANTEE_NAME,'用户名',SCHEMA_NAME,'',OBJECT_NAME,'表名',COLUMN_NAME,'字段名',DATA_TYPE_SIZE,'字段类型/长度',TEXT,'字段描述',TABLE_TEXT,'表描述')
                if OBJECT_NAME == "SB_HISTOGRAM_INTERVALS" or OBJECT_NAME == "SB_HISTOGRAMS" or OBJECT_NAME == "SB_HISTOGRAMS" or OBJECT_NAME == "SB_PERSISTENT_SAMPLES":
                    pass
                else:
                    # 本地库元数据信息初始化
                    db = con(us_depart)
                    cursor = db.cursor()
                    # 判断表是否存在
                    sql = """select us_tableName from savetable where us_tableName = '{0}';""".format(OBJECT_NAME)
                    print(sql)
                    sql_ending = sql.encode(encoding="utf8")
                    cursor.execute(sql_ending)
                    us_tableName = cursor.fetchall()
                    print(us_tableName,'表名')
                    if us_tableName:
                        pass
                    else:
                        # 本地库插入表结构信息
                        sql = """insert into savetable values (null,'{0}','{1}',0);""".format(TABLE_TEXT.strip(),OBJECT_NAME.strip())
                        print(sql)
                        sql_ending = sql.encode(encoding="utf8")
                        cursor.execute(sql_ending)
                        db.commit()
                    # 获取表id
                    sql = """select id from savetable where us_tableName = '{0}';""".format(OBJECT_NAME)
                    print(sql)
                    sql_ending = sql.encode(encoding="utf8")
                    cursor.execute(sql_ending)
                    table_id= cursor.fetchall()[0][0]
                    print(table_id,'表id')
                    db.commit()
                    # 本地库插入字段结构信息
                    sql = """insert into add_field values (null,'{0}','{1}','{2}',0,{3});""".format(COLUMN_NAME.strip(),TEXT.strip(),DATA_TYPE_SIZE.strip(),table_id)
                    print(sql)
                    sql_ending = sql.encode(encoding="utf8")
                    cursor.execute(sql_ending)
                    db.commit()
                    db.close()
                    
    except:
        result = 0

    return JsonResponse({'result':result})




