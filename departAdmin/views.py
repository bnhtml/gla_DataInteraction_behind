from django.shortcuts import render
from django.shortcuts import render
import subprocess
import xml
import logging

import time
import pymysql
from django.contrib.sites import requests
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
import requests

# Create your views here.


# 目录栏显示初始页面
def admin(request,data,user_login_name):
    print('部门页面')
    depart_list = []
    data_num = ''
    request.session["user_login_name"] = user_login_name
    depart = Department.objects.filter(us_dataname=user_login_name)
    print(depart)
    for departs in depart:
        depart = departs.dataname
        print(depart, "*" * 100)

    db = con(user_login_name)
    cursor = db.cursor()
    sql = """select count(*) from dbList;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    dbList_num = cursor.fetchall()[0][0]
    print(dbList_num,'dbList_num')

    sql = """select count(*) from fileList;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    fileList_num = cursor.fetchall()[0][0]
    print(fileList_num,'fileList_num')

    sql = """select count(*) from interfaceList;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    interfaceList_num = cursor.fetchall()[0][0]
    print(interfaceList_num,'interfaceList_num')

    sql = """select count(*) from messageList;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    messageList_num = cursor.fetchall()[0][0]

    sql = """select count(*) from Uservice;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    service_num = cursor.fetchall()[0][0]

    sql = """select count(*) from Uacl;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    acl_num = cursor.fetchall()[0][0]

    sql = """select count(*) from Ucontrols;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    control_num = cursor.fetchall()[0][0]
    db.close()

    db = con('test')
    cursor = db.cursor()
    sql = """select count(*) from Uuser where depart = '{0}';""".format(user_login_name)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    user_num = cursor.fetchall()[0][0]
    print(user_num,'user_num')


    print(messageList_num,'messageList_num')
    total_num = dbList_num+fileList_num+messageList_num+interfaceList_num+service_num+acl_num+control_num+user_num
    data_num = dbList_num+fileList_num+messageList_num+interfaceList_num
    aclcon_num = acl_num+control_num

    depart_list.append({'depart':depart,'dbList_num':dbList_num,'fileList_num':fileList_num,'interfaceList_num':interfaceList_num,'messageList_num':messageList_num,'total_num': total_num,'service_num':service_num,'data_num':data_num,'acl_num':acl_num,'control_num':control_num,'aclcon_num':aclcon_num,'user_num':user_num})
    print(depart_list,'部门管理返回列表')

    return render(request, 'departAdmin/back_admin.html', {'depart': depart_list})


# 三级目录显示页面
def admin_catalog(request):
    firstName_list = []
    # 获取点击的库名并转换成英文
    china_db = request.session.get('user_login_name')
    print(china_db)
    # us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(china_db)
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
            firstName_list.append({"firstName":firstName,'map_path':map_path})
    # # 获取二级目录列表
    # sql = 'select chinese_abb from AdminSecond;'
    # sql_ending = sql.encode(encoding="utf8")
    # cursor.execute(sql_ending)
    # secondName_tuple = cursor.fetchall()
    # for s_tuple in secondName_tuple:
    #     for secondName in s_tuple:
    #         secondName_list.append(secondName)
    # # 获取三级目录列表
    # sql = 'select chinese_abb from AdminThird;'
    # sql_ending = sql.encode(encoding="utf8")
    # cursor.execute(sql_ending)
    # thirdName_tuple = cursor.fetchall()
    # for t_tuple in thirdName_tuple:
    #     for thirdName in t_tuple:
    #         thirdName_list.append(thirdName)
    # print(firstName_list, secondName_list, thirdName_list)
    return render(request, 'departAdmin/admin_catalog.html', {'firstName_list': firstName_list})


# db数据目录展示页面
def db_list(request):
    tb_name = []
    field_info = []
    china_db = request.session.get('user_login_name')
    # us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(china_db)
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
    return render(request, 'departAdmin/db_list.html', {'tb_name': tb_name, 'field_info': field_info})


# 文件通道
def admin_file(request):
    file_list = []
    fileName_list = []
    china_db = request.session.get('user_login_name')
    # us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(china_db)
    cursor = db.cursor()

    sql = """select * from fileName;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_sql = cursor.fetchall()
    for file in set_sql:
        fileName_list.append(file[1])
    print(fileName_list, '55555555555')

    sql = """select * from fileList"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_sql = cursor.fetchall()
    for file_set in set_sql:
        file_list.append({'filename': file_set[1], 'fileIP': file_set[2]})
    return render(request,'departAdmin/admin_file.html', {'file_list': file_list, 'fileName_list': fileName_list})


# 接口通道
def admin_interface(request):
    interface_list = []
    interfaceName_list = []
    china_db = request.session.get('user_login_name')
    # us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(china_db)
    cursor = db.cursor()

    sql = """select * from interfaceName;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_sql = cursor.fetchall()
    for interface in set_sql:
        interfaceName_list.append(interface[1])
    print(interfaceName_list, '55555555555')

    sql = """select * from interfaceList;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_sql = cursor.fetchall()
    for interface_set in set_sql:
        interface_list.append({"interfacename": interface_set[1], "interfaceIP": interface_set[2]})
    return render(request, 'departAdmin/admin_interface.html', {'interface_list': interface_list, 'interfaceName_list': interfaceName_list})


# 消息通道
def admin_ways(request):
    message_list = []
    messageName_list = []
    china_db = request.session.get('user_login_name')
    # us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(china_db)
    cursor = db.cursor()
    sql = """select * from messageName;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_sql = cursor.fetchall()
    for message in set_sql:
        messageName_list.append(message[1])
    print(messageName_list, '55555555555')

    sql = """select * from messageList;"""
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    set_sql = cursor.fetchall()
    print(set_sql)
    for message_set in set_sql:
        message_list.append({'messagename': message_set[1], 'messageIP': message_set[2]})
    print(message_list,'11111111111111111')

    return render(request, 'departAdmin/admin_ways.html', {'message_list': message_list, 'messageName_list': messageName_list})


# 添加sql选项卡
def page_Sql(request):
    return render(request, 'departAdmin/page_Sql.html')


# select生成页面
def sql_admin(request):
    db_list = []
    # 获取点击的库名并转换成英文
    china_db = request.session.get('user_login_name')
    # print(china_db)
    # us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(china_db)
    # print(db)
    cursor = db.cursor()
    # 获取一级目录列表
    sql = 'select * from dbList;'
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    dbs = cursor.fetchall()
    for db in dbs:
        dbIP = db[3]+'/api/db?id='+str(db[0])
        db_list.append({'dbName': db[1], 'dbSql': db[2],'dbIP':dbIP})

    return render(request, 'departAdmin/sql_admin.html',{'db_list':db_list})


def add_feild(request):
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    depname = request.POST.get('depname')
    china_db = request.session.get('user_login_name')
    feild_name = request.POST.get('feild_name')
    feild_desc = request.POST.get('feild_desc')
    feild_type = request.POST.get('feild_typelen')
    feild_key = request.POST.get('feild_key')
    sendlog = ''
    # us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(china_db)
    cursor = db.cursor()
    sql = """select fieldName from add_field where fieldName='{0}';""".format(feild_name)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    user_name = cursor.fetchall()
    if user_name:
        return JsonResponse({'result': 0})
    sql = """insert into add_field values(null,'{0}','{1}','{2}','{3}',0);""".format(feild_name,feild_desc,feild_type,feild_key)
    task = "添加字段"
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con('china_db')
    cursor = db.cursor()
    sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, feild_name, depname,
                                                                                      airTime, endtime, "成功")

    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    cursor.close()
    db.close()

    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, feild_name,
                                                                                           depname,
                                                                                           airTime, endtime,
                                                                                           "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    sendlog = str((task,
                   feild_name,
                   depname,
                   airTime,
                   endtime,
                   '成功'))
    sendLog = send_log(sendlog)

    return JsonResponse({'result':1})


# 将四大通道数据添加到对应数据库中
def type_add(request):
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    depname = request.POST.get('depname')
    print(depname,"*"*100)
    type = request.POST.get('type')
    add_name = request.POST.get('name')
    dataIp = request.POST.get('dataIP')
    sendlog = ''
    china_db = request.session.get('user_login_name')
    # us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(china_db)
    cursor = db.cursor()
    # print(type, '*'*100)
    if type == 'file':

        sql = """select fileName from fileList where fileName='{0}';""".format(add_name)

        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        user_name = cursor.fetchall()
        if user_name:
            return JsonResponse({'result': 0})
        sql ="""insert into fileList values(null,'{0}','{1}',  0);""".format(add_name, dataIp)

        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "插入文件"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con(china_db)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, add_name, depname,
                                                                                               airTime, endtime, "成功")
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, add_name,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
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
        user_name = cursor.fetchall()
        if user_name:
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
        db = con(china_db)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, add_name,
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
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, add_name,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
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
        user_name = cursor.fetchall()
        if user_name:
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
        db = con(china_db)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, add_name,
                                                                                                   depname,
                                                                                                   airTime, endtime,
                                                                                                   "成功")

        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, add_name,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
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


#  三大通道类型
def update_type(request):
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    depname = request.POST.get('depname')
    type = request.POST.get('type')
    old_name = request.POST.get('old_name')
    update_name = request.POST.get('update_name')
    update_dataIP = request.POST.get('update_dataIP')
    china_db = request.session.get('user_login_name')
    # 连接点击的数据库
    db = con(china_db)
    cursor = db.cursor()
    if type == 'file':
        sql = """delete from fileList where fileName='{0}';""".format(old_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        # sql = """select fileName from fileList where fileName='{0}';""".format(update_name)
        # print(sql)
        # sql_ending = sql.encode(encoding="utf8")
        # cursor.execute(sql_ending)
        # file_name = cursor.fetchall()
        # if file_name:
        #     return JsonResponse({'result': 0})
        sql = """insert into fileList values(null,'{0}','{1}',  0);""".format(update_name, update_dataIP)
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "修改文件"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con(china_db)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, update_name,
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
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, update_name,
                                                                                               depname,
                                                                                               airTime, endtime,
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

        return JsonResponse({'result': 1})
    elif type == 'interface':
        sql = """delete from interfaceList where interfaceName='{0}';""".format(old_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        #
        # sql = """select interfaceName from interfaceList where interfaceName='{0}';""".format(update_name)
        # sql_ending = sql.encode(encoding="utf8")
        # cursor.execute(sql_ending)
        # user_name = cursor.fetchall()
        # if user_name:
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
        db = con(china_db)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, update_name,
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
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, update_name,
                                                                                               depname,
                                                                                               airTime, endtime,
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

        return JsonResponse({'result': 1})

    elif type == 'ways':
        sql = """delete from messageList where messageName='{0}';""".format(old_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)

        sql = """select messageName from messageList where messageName='{0}';""".format(update_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        user_name = cursor.fetchall()
        if user_name:
            return JsonResponse({'result': 0})
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
        db = con(china_db)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, update_name,
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
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, update_name,
                                                                                               depname,
                                                                                               airTime, endtime,
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

        return JsonResponse({'result': 1})


# 删除三大通道
def del_type(request):
    depname = request.POST.get('depname')
    type = request.POST.get('type')
    name = request.POST.get('name')
    print(type)
    sendlog = ''
    china_db = request.session.get('user_login_name')
    # us_china = getPinyin(china_db)
    # 连接点击的数据库
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con(china_db)
    cursor = db.cursor()
    # print(type, '*'*100)
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
        db = con(china_db)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, name,
                                                                                                   depname,
                                                                                                   airTime, endtime,
                                                                                                   "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, name,
                                                                                               depname,
                                                                                               airTime, endtime,
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
        db = con(china_db)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, name,
                                                                                                   depname,
                                                                                                   airTime, endtime,
                                                                                                   "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, name,
                                                                                               depname,
                                                                                               airTime, endtime,
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
        db = con(china_db)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, name,
                                                                                                   depname,
                                                                                                   airTime, endtime,
                                                                                                   "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, name,
                                                                                               depname,
                                                                                               airTime, endtime,
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


# 管理员页面添加数据表
def add_table(request):

    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    depname = request.POST.get('depname')
    table_ch = request.POST.get('table_ch')
    table_en = request.POST.get('table_en')
    china_db = request.session.get('user_login_name')
    # us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(china_db)
    cursor = db.cursor()

    sql = """select tableName from savetable where tableName='{0}';""".format(table_ch)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    user_name = cursor.fetchall()
    if user_name:
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
    db = con(china_db)
    cursor = db.cursor()
    sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, table_ch,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, table_ch,
                                                                                           depname,
                                                                                           airTime, endtime,
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
    depname = request.POST.get('depname')
    table_name = request.POST.get('table_name')
    field_name = request.POST.get('field_name')
    field_desc = request.POST.get('field_desc')
    field_type = request.POST.get('field_type')
    china_db = request.session.get('user_login_name')
    sendlog = ''
    # 连接点击的数据库
    db = con(china_db)
    cursor = db.cursor()
    sql = """select id from savetable where  us_tableName='{0}';""".format(table_name)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    dbs = cursor.fetchall()[0][0]
    # print(dbs,'*'*200)

    sql = """select fieldName from add_field where fieldName='{0}' and tableKey_id={1};""".format(field_name,dbs)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    user_name = cursor.fetchall()
    if user_name:
        return JsonResponse({'result': 0})
    sql = """insert into add_field values(null, '{0}', '{1}', '{2}', 0, '{3}');""".format( field_name,  field_desc, field_type, dbs)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    task = "添加字段"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con(china_db)
    cursor = db.cursor()
    sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, field_name,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, field_name,
                                                                                           depname,
                                                                                           airTime, endtime,
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
    china_db = request.session.get('user_login_name')
    # us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(china_db)
    cursor = db.cursor()
    sql = """select id from savetable where  us_tableName='{0}';""".format(tableName)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    dbs = cursor.fetchall()
    sql = """select * from add_field where tableKey_id={0};""".format(dbs[0][0])
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    field_list = cursor.fetchall()
    for field in field_list:
        field_info.append({'fieldName': field[1], 'fieldDesc': field[2], 'fieldType': field[3]})
    # print(field_info, '*'*100)
    return JsonResponse({'result': field_info})


# 数据源删除数据表
def table_delete(request):
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    depname = request.POST.get('depname')
    sendlog = ''
    tb_id = ''
    china_db = request.session.get('user_login_name')
    table_en = request.POST.get('table_en')
    print(table_en)

    # 连接点击的数据库
    db = con(china_db)
    cursor = db.cursor()
    sql = """select id from savetable where us_tableName='{0}';""".format(table_en)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    tb_id = cursor.fetchall()[0][0]
    sql = """delete from add_field where tableKey_id={0};""".format(tb_id)

    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    sql = """delete from savetable where us_tableName='{0}';""".format(table_en)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    task = "删除数据表"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con(china_db)
    cursor = db.cursor()
    sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, table_en,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, table_en,
                                                                                           depname,
                                                                                           airTime, endtime,
                                                                                           "成功")
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

    return JsonResponse({'result':1})


# sql页面获取数据
def get_table(request):
    get_table = []
    result = []
    china_db = request.session.get('user_login_name')
    # us_china = getPinyin(china_db)
    # 连接点击的数据库
    db = con(china_db)
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
    return JsonResponse({'result':get_table })


# 数据源删除字段操作
def field_delete(request):
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    table_id = ''
    depname = request.POST.get('depname')
    field_name = request.POST.get('fieldname')
    china_db = request.session.get('user_login_name')
    # us_china = getPinyin(china_db)

    # 连接点击的数据库
    db = con(china_db)
    cursor = db.cursor()
    sql = """select tableKey_id from add_field where fieldName='{0}';""".format(field_name)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    table_ids = cursor.fetchall()
    for table_ids in table_ids:
        table_id = table_ids[0]
    sql = """delete from add_field where fieldName='{0}' and tableKey_id={1};""".format(field_name,table_id)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    task = "删除字段"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con(china_db)
    cursor = db.cursor()
    sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, field_name,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, field_name,
                                                                                           depname,
                                                                                           airTime, endtime,
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


# 数据源修改表名
def update_table(request):
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    depname = request.POST.get('depname')
    china_db = request.session.get('user_login_name')
    old_table_ch = request.POST.get("old_table_ch")
    table_ch = request.POST.get("table_ch")
    table_en = request.POST.get("table_en")

    # 连接点击的数据库
    db = con(china_db)
    cursor = db.cursor()

    # sql = """select tableName from savetable where tableName='{0}';""".format(table_ch)
    # print(sql)
    # sql_ending = sql.encode(encoding="utf8")
    # cursor.execute(sql_ending)
    # user_name = cursor.fetchall()
    # print(user_name)
    # if user_name:
    #     return JsonResponse({'result': 0})
    sql = """update savetable set tableName='{0}',us_tableName='{1}' where tableName='{2}';""".format(table_ch,table_en,old_table_ch)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    task = "修改数据表"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con(china_db)
    cursor = db.cursor()
    sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, table_ch,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()
    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, table_ch,
                                                                                           depname,
                                                                                           airTime, endtime,
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
    depname = request.POST.get('depname')
    sendlog = ''
    china_db = request.session.get('user_login_name')
    old_field_name = request.POST.get("old_fieldname")
    field_name = request.POST.get("field_name")
    field_desc = request.POST.get("field_desc")
    field_type = request.POST.get("field_type")

    print(old_field_name,"*"*100)

    # 连接点击的数据库
    db = con(china_db)
    cursor = db.cursor()

    sql = """select tableKey_id from add_field where fieldName='{0}';""".format(old_field_name)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    tables = cursor.fetchall()
    for table in tables:
        table_id = table[0]

    # sql = """select fieldName from add_field where fieldName='{0}' and tableKey_id={1};""".format(field_name,table_id)
    # sql_ending = sql.encode(encoding="utf8")
    # cursor.execute(sql_ending)
    # user_name = cursor.fetchall()
    # if user_name:
    #     return JsonResponse({'result': 0})
    sql = """update add_field set fieldName='{0}',fieldDesc='{1}',fieldType='{2}' where fieldName='{3}';""".format(field_name,field_desc,field_type,old_field_name)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    task = "修改字段"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con(china_db)
    cursor = db.cursor()
    sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, field_name,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, field_name,
                                                                                           depname,
                                                                                           airTime, endtime,
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


# 三级目录更新操作
def update_catalog(request):
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    depname = request.POST.get('depname')
    firstId_list = []
    secondId_list = []
    thirdId_list = []
    result = []
    sendlog = ''
    update_name = request.POST.get('update_name')
    us_name = getPinyin(update_name)
    table_name = request.POST.get('dier')
    old_name = request.POST.get('old_name')

    if table_name == '一级目录':
        # 获取点击的库名并转换成英文
        user_login_name = request.session.get('user_login_name')
        db = con(user_login_name)
        # print(db)
        cursor = db.cursor()
        sql = """select id from AdminFirst where chinese_abb='{0}';""".format(old_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        first_tuple = cursor.fetchall()
        for f_tup in first_tuple:
            for first_id in f_tup:
                firstId_list.append(first_id)
        # sql = """select chinese_abb from AdminFirst where chinese_abb='{0}';""".format(update_name)
        # sql_ending = sql.encode(encoding="utf8")
        # cursor.execute(sql_ending)
        # select_name = cursor.fetchall()
        # if select_name:
        #     result.append({'result': 0, 'us_updateName': 0})
        #     return JsonResponse({'result': result})
        sql = """update AdminFirst set chinese_abb='{0}' where id={1};""".format(update_name, firstId_list[0])
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)

        sql = """update AdminFirst set department='{0}' where id={1};""".format(us_name, firstId_list[0])
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)

        db.commit()
        db.close()


        task = "修改一级目录"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con(user_login_name)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, update_name,
                                                                                                   depname,
                                                                                                   airTime, endtime,
                                                                                                   "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, update_name,
                                                                                               depname,
                                                                                               airTime, endtime,
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
        user_login_name = request.session.get('user_login_name')
        db = con(user_login_name)
        # print(db)
        cursor = db.cursor()
        sql = """select first_id from AdminSecond where chinese_abb='{0}';""".format(old_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        first_ids = cursor.fetchall()
        for first_i in first_ids:
            first_id = first_i[0]

        sql = """select id from AdminSecond where chinese_abb='{0}';""".format(old_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        second_tuple = cursor.fetchall()
        for s_tup in second_tuple:
            for second_id in s_tup:
                secondId_list.append(second_id)

        # sql = """select chinese_abb from AdminSecond where chinese_abb='{0}' and first_id={1};""".format(update_name,first_id)
        # sql_ending = sql.encode(encoding="utf8")
        # cursor.execute(sql_ending)
        # select_name = cursor.fetchall()
        # if select_name:
        #     result.append({'result': 0, 'us_updateName': 0})
        #     return JsonResponse({'result': result})
        sql = """update AdminSecond set chinese_abb='{0}' where id={1};""".format(update_name, secondId_list[0])
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
       
        sql = """update AdminSecond set industry='{0}' where id={1};""".format(us_name, secondId_list[0])
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)

        db.commit()
        db.close()

        task = "修改二级目录"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con(user_login_name)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, update_name,
                                                                                                   depname,
                                                                                                   airTime, endtime,
                                                                                                   "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, update_name,
                                                                                               depname,
                                                                                               airTime, endtime,
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
        user_login_name = request.session.get('user_login_name')
        db = con(user_login_name)
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

        # sql = """select chinese_abb from AdminThird where chinese_abb='{0}' and second_id={1};""".format(update_name,id)
        # sql_ending = sql.encode(encoding="utf8")
        # cursor.execute(sql_ending)
        # select_name = cursor.fetchall()
        # if select_name:
        #     result.append({'result': 0, 'us_updateName': 0})
        #     return JsonResponse({'result': result})
        sql = """update AdminThird set chinese_abb='{0}' where id={1}; """.format(update_name, secondId_list[0])
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)

        sql = """update AdminThird set species='{0}' where id={1}; """.format(us_name, secondId_list[0])
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "修改三级目录"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con(user_login_name)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, update_name,
                                                                                                   depname,
                                                                                                   airTime, endtime,
                                                                                                   "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, update_name,
                                                                                               depname,
                                                                                               airTime, endtime,
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


# 三级目录删除操作
def delete_catalog(request):
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    id = ''
    depname = request.POST.get('depname')
    catalog_name = request.POST.get('delete_name')
    table_name = request.POST.get('dier')
    user_login_name = request.session.get('user_login_name')
    sendlog = ''

    if table_name == '一级目录':
        # 获取点击的库名并转换成英文
        user_login_name = request.session.get('user_login_name')
        db = con(user_login_name)
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
        db = con(user_login_name)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, catalog_name,
                                                                                                   depname,
                                                                                                   airTime, endtime,
                                                                                                   "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, catalog_name,
                                                                                               depname,
                                                                                               airTime, endtime,
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
        user_login_name = request.session.get('user_login_name')
        db = con(user_login_name)
        # print(db)
        cursor = db.cursor()

        sql = """select first_id from AdminSecond where chinese_abb='{0}'""".format(catalog_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        first_ids = cursor.fetchall()
        for first_i in first_ids:
            first_id = first_i[0]

        sql = """select id from AdminSecond where chinese_abb='{0}'""".format(catalog_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        sql_id = cursor.fetchall()
        for ids in sql_id:
            id = ids[0]

        sql = """delete from AdminThird where second_id = {0};""".format(id)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)


        sql = """delete from AdminSecond where chinese_abb='{0}' and first_id={1}""".format(catalog_name,first_id)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "删除二级目录"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con(user_login_name)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, catalog_name,
                                                                                                   depname,
                                                                                                   airTime, endtime,
                                                                                                   "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, catalog_name,
                                                                                               depname,
                                                                                               airTime, endtime,
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
        user_login_name = request.session.get('user_login_name')
        db = con(user_login_name)
        # print(db)
        cursor = db.cursor()

        sql = """select second_id from AdminThird where chinese_abb='{0}'""".format(catalog_name)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        sql_id = cursor.fetchall()
        for ids in sql_id:
            id = ids[0]

        sql = """delete from AdminThird where chinese_abb='{0}' and second_id={1}""".format(catalog_name,id)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        task = "删除三级目录"
        endtime = time.time()
        timeArray = time.localtime(endtime)
        endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        db = con(user_login_name)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, catalog_name,
                                                                                                   depname,
                                                                                                   airTime, endtime,
                                                                                                   "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

        db = con("test")
        cursor = db.cursor()
        sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, catalog_name,
                                                                                               depname,
                                                                                               airTime, endtime,
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


# 获取一级目录内容
def catalog_info(request):
    depname = request.POST.get('depname')
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    result = []
    # 获取一级目录名称
    first_info = request.POST.get('first_name')
    # print(first_info)
    en_first = getPinyin(first_info)
    # 获取点击的库名并转换成中文
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
    # print(db)
    cursor = db.cursor()

    sql = """select chinese_abb from AdminFirst where chinese_abb='{0}';""".format(first_info)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    user_name = cursor.fetchall()
    if user_name:
        result.append({'result': 0, 'map_path': 0})
        return JsonResponse({'result': result})
    sql = """insert into AdminFirst values (null,"{0}","{1}",0);""".format(
             en_first, first_info)
    # print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    task = "添加一级目录"
    endtime = time.time()
    timeArray = time.localtime(endtime)
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    db = con(user_login_name)
    cursor = db.cursor()
    sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, first_info,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, first_info,
                                                                                           depname,
                                                                                           airTime, endtime,
                                                                                           "成功")
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
    result.append({'result':1,'map_path':map_path})
    return JsonResponse({'result': result})


def second_info(request):
    depname = request.POST.get('depname')
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    first_list = []
    result = []
    firstInfo = request.POST.get('first_name')
    secondInfo = request.POST.get('second_name')
    # 获取英文简称
    en_second = getPinyin(secondInfo)
    # 获取点击的库名并转换成英文
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
    # print(db)
    cursor = db.cursor()
    sql = """select id from AdminFirst where chinese_abb='{0}';""".format(firstInfo)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    first_tuple = cursor.fetchall()
    for F_tuple in first_tuple:
        for first_id in F_tuple:
            first_list.append(first_id)

    sql = """select chinese_abb from AdminSecond where chinese_abb='{0}' and first_id='{1}';""".format(secondInfo,first_list[0])
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    user_name = cursor.fetchall()
    if user_name:
        result.append({'result': 0, 'map_path': 0})
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
    db = con(user_login_name)
    cursor = db.cursor()
    sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, secondInfo,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, secondInfo,
                                                                                           depname,
                                                                                           airTime, endtime,
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
    depname = request.POST.get('depname')
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    firstList = []
    secondList = []
    result = []
    firstInfo = request.POST.get('first_name')
    secondInfo = request.POST.get('second_name')
    thirdInfo = request.POST.get('third_name')
    # print(firstInfo, secondInfo, thirdInfo)
    # 将三级目录转化成英文简称
    en_third = getPinyin(thirdInfo)
    # 获取点击的库名并转换成英文
    user_login_name = request.session.get('user_login_name')
    us_china = user_login_name
    db = con(user_login_name)
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
    print(1)
    sql = """select id from AdminSecond where chinese_abb='{0}';""".format(secondInfo)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    second_tuple = cursor.fetchall()
    for S_tuple in second_tuple:
        for second_id in S_tuple:
            secondList.append(second_id)
    # print(secondList)

    sql = """select chinese_abb from AdminThird where chinese_abb='{0}'  and second_id={1};""".format(thirdInfo,secondList[0])
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    user_name = cursor.fetchall()
    if user_name:
        result.append({'result': 0, 'map_path': 0})
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
    db = con(user_login_name)
    cursor = db.cursor()
    sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, thirdInfo,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, thirdInfo,
                                                                                           depname,
                                                                                           airTime, endtime,
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
    print(result)
    return JsonResponse({'result': result})


# 获取二级目录信息
def second_list(request):

    first_list = []
    secondName_list = []
    # 获取选中的一级目录名称
    first_name = request.POST.get('first_name')
    # 获取点击的库名并转换成英文
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
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
            secondName_list.append({'secondName':secondName,'us_secondName':us_secondName})
    return JsonResponse({'data': secondName_list})


# 获取三级目录信息
def third_list(request):
    secondList = []
    secondName_list = []
    # 获取选中的二级目录
    second_name = request.POST.get('second_name')
    # 获取点击的库名并转换成英文
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
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
            secondName_list.append({'thirdName':thirdName,'us_thirdName':us_thirdName})

    return JsonResponse({'data': secondName_list})


# 三级目录显示页面
def admin_catalog(request):
    firstName_list = []
    # 获取点击的库名并转换成英文
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
    cursor = db.cursor()
    # 获取一级目录列表
    sql = 'select chinese_abb from AdminFirst;'
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    firstName_tuple = cursor.fetchall()
    for f_tuple in firstName_tuple:
        for firstName in f_tuple:
            map_path = getPinyin(firstName)
            firstName_list.append({"firstName":firstName,'map_path':map_path})
    # # 获取二级目录列表
    # sql = 'select chinese_abb from AdminSecond;'
    # sql_ending = sql.encode(encoding="utf8")
    # cursor.execute(sql_ending)
    # secondName_tuple = cursor.fetchall()
    # for s_tuple in secondName_tuple:
    #     for secondName in s_tuple:
    #         secondName_list.append(secondName)
    # # 获取三级目录列表
    # sql = 'select chinese_abb from AdminThird;'
    # sql_ending = sql.encode(encoding="utf8")
    # cursor.execute(sql_ending)
    # thirdName_tuple = cursor.fetchall()
    # for t_tuple in thirdName_tuple:
    #     for thirdName in t_tuple:
    #         thirdName_list.append(thirdName)
    # print(firstName_list, secondName_list, thirdName_list)
    return render(request, 'departAdmin/admin_catalog.html', {'firstName_list': firstName_list})


#sql写入文件
def update_data(request):
    depname = request.POST.get('depname')
    user_login_name = request.session.get('user_login_name')
    airTime = time.time()
    timeArray = time.localtime(airTime)
    airTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    sendlog = ''
    # 连接点击的数据库
    db = con(user_login_name)
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
    db = con(user_login_name)
    cursor = db.cursor()
    sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, field_name,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    db = con("test")
    cursor = db.cursor()
    sql = """insert into mylog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, field_name,
                                                                                           depname,
                                                                                           airTime, endtime,
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

    return JsonResponse({'result':1})


# 添加sql选项卡
def page_Sql(request):
    return render(request, 'departAdmin/page_Sql.html')


# 添加sql选项卡
def sql_name(request):
    return render(request, 'departAdmin/sql_name.html')


# 生成sql页面
def sql_append(request):
    return render(request, 'departAdmin/sql_append.html')


# sql语句保存操作
# sql语句保存操作
def sql_save(request):
    depname = request.POST.get('depname')
    sql_name = request.POST.get('sql_name')
    sql = request.POST.get('get_sql')
    sql1 = sql.replace(",", "$")
    sql_ip = request.POST.get('sql_ip')
    user_login_name = request.session.get('user_login_name')
    sqlIp=""
    if sql_name == '' or sql == '':
        return JsonResponse({'res': 0})
        # print(sql_name, sql)
    else:
        i = 0
        with open("./sql_file/count.txt", "r") as f:
            strcount = f.read()
            i = int(strcount)
        # if "bass" in sql_ip:
        #     sqlIp1 = sql_ip.replace("bass","1.255.1.202")
        #     sqlIp = sqlIp1 +'?id={0}'.format(str(i))
        if sql_ip == 'mysql':
            sqlIp1 = "http://1.255.1.202:3000/api/db"
            sqlIp = sqlIp1 + '?id={0}'.format(str(i))
        elif sql_ip == 'oracle':
            sqlIp1 = "http://1.255.1.202:3001/api/db"
            sqlIp = sqlIp1 + '?id={0}'.format(str(i))
        elif sql_ip == '国家接口':
            sqlIp1 = "http://1.255.1.202:3002/api/db"
            sqlIp = sqlIp1 + '?id={0}'.format(str(i))
        elif sql_ip == '大数据':
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
        # 获取点击的库名并转换成英文
        # us_china = getPinyin(user_login_name)
        db = con(user_login_name)
        # print(db)
        cursor = db.cursor()
        # sql = """select dbName from dbList where dbName='{0}';""".format(sql_name)
        # sql_ending = sql.encode(encoding="utf8")
        # cursor.execute(sql_ending)
        # tb_name = cursor.fetchall()
        # print(tb_name,'*'*100)
        # if tb_name:
        #     return JsonResponse({'result': 0})
        sql = """insert into dbList values(null, '{0}', '{1}','{2}', 0);""".format(sql_name, sql,sqlIp)
        print(sql, '&' * 100)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()
        with open("./sql_file/db.detail.sql", "a+") as f:
            detail="桥接名称："+ sql_name +"  "+"数据区："+sql_ip+"  "+"sql语句："+sql1
            f.write(detail+"\n")
        return JsonResponse({'result': 1})
        return JsonResponse({'result': 1})


# 数据桥接修改
def sql_update(request):

    dbname = request.POST.get("dbname")
    sql_name = request.POST.get("sql_name")
    sql_ip = request.POST.get("sql_ip")
    get_sql = request.POST.get("get_sql")
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
    # print(db)
    cursor = db.cursor()

    # sql = """select dbName from dbList where dbName='{0}';""".format(dbname)
    # sql_ending = sql.encode(encoding="utf8")
    # cursor.execute(sql_ending)
    # user_name = cursor.fetchall()
    # if user_name:
    #     return JsonResponse({"result": 0})
    sql = """update dbList set dbName='{0}',dbSql='{1}',dbIP='{2}' where dbName='{3}'""".format(sql_name, get_sql, sql_ip,dbname)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

    return JsonResponse({"result":1})


# 删除sql语句
def delete_db(request):
    delete_name = request.POST.get('delete_name')
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
    cursor = db.cursor()
    sql = """delete from dbList where dbName='{0}';""".format(delete_name)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()
    return JsonResponse({'result': 1})


def desc_show(request, db_name):
    # db_name = []
    db_id = ''
    us_table = []
    field_info = []
    # us_china = getPinyin(china_db)
    # 连接点击的数据库
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
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
        field_info.append({'fieldName': field[1], 'fieldDesc': field[2],'field_type':field[3],"us_table":us_table})
    # print(field_info, '*'*100)
    return JsonResponse({'data': field_info})


# 文件源录入页面显示
def file_list(request):

    file_name = []
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
    cursor = db.cursor()
    sql = """select * from fileName;"""
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    filename = cursor.fetchall()
    for file_Name in filename:

        file_name.append(file_Name[1])
    print(file_name)
    # print(file_Name[1])

    return render(request, 'departAdmin/file_list.html', {'file_name': file_name})


# 接口源录入页面显示
def interface_list(request):

    interface_name = []
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
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

    return render(request, 'departAdmin/interface_list.html', {'interface_name': interface_name})


# 消息源录入页面显示
def message_list(request):

    message_name = []
    user_login_name = request.session.get('user_login_name')
    db = con(user_login_name)
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

    return render(request, 'departAdmin/message_list.html', {'message_name': message_name})


# 获取元数据参数
def meta_list(request):

    depname = request.POST.get('depname')  # 部门
    metatype = request.POST.get('metatype')  # 数据元表（接口、文件、消息）
    mename = request.POST.get('tableName')  # 数据元名称
    print(depname,'*'*100)
    print(metatype,'&'*100)
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

    sql = """select * from {0} where {1} = '{2}';""".format(partable, meta_id, me_id)
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
        db = con(us_china)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, tableName,
                                                                                                   depname,
                                                                                                   airTime, endtime,
                                                                                                   "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

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

        db = con(us_china)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, par_name,
                                                                                                   depname,
                                                                                                   airTime, endtime,
                                                                                                   "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

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

        db = con(us_china)
        cursor = db.cursor()
        sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, newmename,
                                                                                                   depname,
                                                                                                   airTime, endtime,
                                                                                                   "成功")
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()

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

    db = con(us_china)
    cursor = db.cursor()
    sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, newpar_name,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

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

    db = con(us_china)
    cursor = db.cursor()
    sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, mename,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

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

    db = con(us_china)
    cursor = db.cursor()
    sql = """insert into departlog values(null,'{0}','{1}','{2}','{3}','{4}','{5}');""".format(task, par_name,
                                                                                               depname,
                                                                                               airTime, endtime,
                                                                                               "成功")
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    db.close()

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

    return render(request, 'departAdmin/user_list.html', {'Uuser': Uuser_list})


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
                'departAdmin/service_list.html',
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
    sql =  """select username from Uuser where depart = '{0}';""".format(user_login_name)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    Uusers = cursor.fetchall()
    for Uuser in Uusers:
        print(Uuser[0])
        Uuser_list.append(Uuser[0])
    print(Uuser_list)
    db.commit()
    db.close()

    return render(request, 'departAdmin/acl_list.html', {'Uacl': Uacl_list, 'Aacl': Aacl_list, 'Uuser': Uuser_list})


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
    sql = """select username from Uuser;"""
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

    return render(request, 'departAdmin/control_list.html', {'Ucontrol': Ucontrol_list, 'username': user_list, 'servicename': servicename_list})