import os
import requests
from django.shortcuts import render
# Create your views here
import pymysql
from uti.db_connect import con
from uti.db_connect import middle_con
from django.http import JsonResponse, HttpResponse
from urllib import request


def index(request):
    # 海云列表
    resourceId_list = []
    # 中软列表
    resourceID_list = []
    db = con("test")
    cursor = db.cursor()
    # 海云查询
    sql = """select resourceId from hyParticipation where isTransact = 1;"""
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    resourceIdSet = cursor.fetchall()
    for one in resourceIdSet:
        for two in one:
            resourceId_list.append(two)

    # 中软查询
    sql = """select resourceId from noticedata where isTransact = 1;"""
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    resourceIdSet = cursor.fetchall()
    for one in resourceIdSet:
        for two in one:
            resourceID_list.append(two)
    db.commit()
    db.close()
    print(resourceId_list)
    return render(request,'controlCenter/controlCenter.html', {"resourceId_list": resourceId_list, "resourceID_list":resourceID_list})
    # return render(request, 'controlCenter/controlCenter.html')


# 代办事项处理
def isTransact(request):
    print(1)
    if request.method == "POST":
        tableName = request.POST.get("tableName")
        resourceID = request.POST.get("resourceID")
        print(resourceID)
        db =con("test")
        cursor = db.cursor()
        sql = """update {0} set isTransact = 0 where resourceId = '{1}';""".format(tableName,resourceID)
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()
        return JsonResponse({'result': 1})


# 数据目录信息插入中间库
def insert_mysql(request):
    print("数据目录信息插入中间库")
    status_code = 1
    if request.method == "POST":
        resource_id= request.POST.get("resource_id")
        print(resource_id, 'resource_id')
        dictionary_address = request.POST.get("dictionary_address")
        print(dictionary_address, 'dictionary_address')
        file_id = request.POST.get("file_id")
        print(file_id,'file_id')
        request_data_type = request.POST.get("request_data_type")
        print(request_data_type,'request_data_type')
        response_data_type = request.POST.get("response_data_type")
        print(response_data_type,'response_data_type')
        request_type = request.POST.get("request_type")
        print(request_type,'request_type')
        request_head = request.POST.get("request_head")
        print(request_head,'request_head')
        print(status_code,'status_code')
        description = request.POST.get("description")
        print(description,'description')
        data_name = request.POST.get("data_name")
        print(data_name,'data_name')
        depart_name = request.POST.get("depart_name")
        print(depart_name,'depart_name')
        intResource_id=int(resource_id)
        print(intResource_id,'intResource_id')
        intFile_id = int(file_id)
        print(intFile_id,'intFile_id')
        intStatus_code = int(status_code)
        print(intResource_id)
        db = middle_con("datamarket")
        cursor = db.cursor()
        print(1)
        sql = """insert into interface_description values ({0},'{1}',{2},'{3}','{4}','{5}','{6}',{7},'{8}','{9}','{10}');""".format(
            intResource_id, dictionary_address, intFile_id, request_data_type,response_data_type,request_type,request_head,intStatus_code,description,data_name,depart_name)
        # sql = """insert into interface_description values ({0},'{1}',{2},'{3}','{4}','{5}','{6}',{7},'{8}','{9}','{10}');""".format(1, "http://www.baidu.com",11, "json","json","post","application/json",1,"百度","接口查询","大数据局")
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        db.commit()
        db.close()
        # requests.get('http://192.168.31.137:8080/fileUpload/fileUpload', )
        return JsonResponse({"result": 1})


# 通知海云数据资源上架成功
def tell_hy_successed(request):
    print("通知海云数据资源上架成功")
    if request.method == "POST":
        resourceId = request.POST.get('resourceId')
        data ={
            "resourceId": resourceId
        }
        print(resourceId,'resourceId')
        html = requests.request(method="POST", url="http://192.168.41.15:8080/thirdParty/shareExchange/successFeedback", data=data)
        print(html.text)
    return JsonResponse({"result": 1})


# 向海云服务器提交文件
def commitFile(request):
    if request.method == "POST":
        file = request.FILES.get("myFile", None)  # 接收上传的文件
        path = '/home/mamba/local/'  # 创建文件存储路径
        if not os.path.exists(path):
            os.makedirs(path)  # 创建存储文件的文件夹
        if not file:
            return HttpResponse("no files for upload!")
        destination = open(os.path.join(path, file.name), 'wb')
        for chunk in file.chunks():
            destination.write(chunk)
            destination.close()
            pathloal = path+file.name
            # with open(pathloal, "b") as f:
            #     a = f.read()
            file = {'file': open(pathloal, 'rb')}
            reque = requests.post('http://192.168.41.15:8080/fileUpload/fileUpload', files=file)
            print(reque.text)
            print(reque.content)
            return JsonResponse({"result": reque.content})
