# -*- coding: utf-8 -*
from django.contrib.sites import requests
from django.shortcuts import render
from django.http import JsonResponse
from Safe_dic.models import *
from uti.db_connect import con

# Create your views here.

# 获取安全目录数据
# def save_list(request):
#     save_list = []
#     saves = SaveData.objects.using('Safe_dic').all()
#     for saves in saves:
#         save_list.append({'username':saves.username,
#                           'dataname':saves.dataname,
#                           'access_control':saves.access_control,
#                           'flow_control':saves.flow_control,
#                           })
#     print(save_list)
#
#     return render(request, 'superAdmin/save_list.html',{'saves':save_list})
#
#
# # 添加安全目录数据
# def add_save(request):
#     username = request.POST.get('username')
#     dataname = request.POST.get('dataname')
#     access_control = request.POST.get('access_control')
#     flow_control = request.POST.get('flow_control')
#
#     obj = SaveData.objects.create(id=None,
#                                   username=username,
#                                   dataname=dataname,
#                                   access_control=access_control,
#                                   flow_control=flow_control,
#                                   is_delete=0,
#                                   )
#
#     obj.save(using='Safe_dic')
#     return JsonResponse({'result':1})
#
#
# # 删除安全目录数据
# def del_save(request):
#     username = request.POST.get('username')
#     obj = SaveData.objects.using('Safe_dic').get(username=username)
#     obj.delete()
#     return JsonResponse({'result':1})


# 查询安全目录信息接口
def findControl(request, args=None):
    db = con('Save_dic')
    cursor = db.cursor()
    if args is None:
        sql = """select * from accesscontrol """
        sql_ending = sql.encode(encoding="utf8")
        # print(sql)
        cursor.execute(sql_ending)
        controls = cursor.fetchall()
        return JsonResponse({'result': controls})
    else:
        sql = """select * from accesscontrol where  serviceName  ='{0}'; """.format(args)
        sql_ending = sql.encode(encoding="utf8")
        # print(sql)
        cursor.execute(sql_ending)
        controls = cursor.fetchall()
        return JsonResponse({'result': controls})


# 查询流控接口
def findFlow(request, args=None):
    db = con('Save_dic')
    cursor = db.cursor()
    if args is None:
        sql = """select * from flowcontrol """
        sql_ending = sql.encode(encoding="utf8")
        # print(sql)
        cursor.execute(sql_ending)
        flows = cursor.fetchall()
        return JsonResponse({'result': flows})
    else:
        sql = """select * from flowcontrol where  serviceName  ='{0}'; """.format(args)
        sql_ending = sql.encode(encoding="utf8")
        # print(sql)
        cursor.execute(sql_ending)
        flows = cursor.fetchall()
        return JsonResponse({'result': flows})


# 查询用户接口
def findUser(request, args=None):
    db = con('Save_dic')
    cursor = db.cursor()
    if args is None:
        sql = """select * from  user """
        sql_ending = sql.encode(encoding="utf8")
        # print(sql)
        cursor.execute(sql_ending)
        users = cursor.fetchall()
        return JsonResponse({'result': users})
    else:
        sql = """select * from user where  username  ='{0}'; """.format(args)
        sql_ending = sql.encode(encoding="utf8")
        # print(sql)
        cursor.execute(sql_ending)
        users = cursor.fetchall()
        return JsonResponse({'result': users})





