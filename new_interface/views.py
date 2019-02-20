from django.shortcuts import render

# Create your views here.
# 与vue交互
from urllib import request
# 调用分页函数
from commonUser.views import page_nation_vue
from uti.db_connect import con
from uti.usercode import getPinyin
from django.http import JsonResponse


# -----------------系统管理 -------------------

# 返回格式
# --正常获取数据
def result(data):

    Result = {
        "msg": "success",  # 类型：String  必有字段  备注：无
        "result": {  # 类型：Object  必有字段  备注：无

            "data":data,
        },
        "code": 200  # 类型：Number  必有字段  备注：无
    }

    return Result


# --分页获取数据
def result1(data,page):

    Result = {
        "msg": "success",  # 类型：String  必有字段  备注：无
        "result": {  # 类型：Object  必有字段  备注：无

            "data": data,
            "page":page,
        },
        "code": 200  # 类型：Number  必有字段  备注：无
    }

    return Result


# --操作成功
def result2(data):

    Result = {
        "msg":"success",
        "result":{
            "status":200,
            "msg":data,
        },
        "code":200
    }

    return Result


# --请求方式报错
def result3(data,status):

    Result = {
        "Status": status,  # --错误码
        "msg": data,  # --错误描述
        "result": "",  # --返回的数据
    }

    return Result


# -接口路径管理
# --获取一级目录信息
# --获取一级目录信息
def get_firstdir(request):
    data = []
    if request.method == "POST":
        depart = request.POST.get('depart')
        if depart:
            print(depart,'部门')
            # 转义
            us_china = getPinyin(depart)
            # 连接数据库
            db = con(us_china)
            cursor = db.cursor()
            # 获取一级目录id
            sql = """select * from AdminFirst """
            print(sql)
            sql_ending = sql.encode(encoding="utf8")
            cursor.execute(sql_ending)
            firstdir = cursor.fetchall()
            print(firstdir,'firstdir')
            for firstDir in firstdir:
                print(firstDir,'firstDir')
                data.append({"first_dir":firstDir[2],"firstdir_mapping":firstDir[1]})

            Result = result(data)
        else:
            status = 500
            data = "depart传参有误"
            Result = result3(data,status)
    else:
        status = 404
        data = "该请求方式为POST请求"
        Result = result3(data,status)

    return JsonResponse( Result )


# --获取二级目录信息
def get_seconddir(request):
    if request.method == "POST":
        first_list = []
        secondName_list = []
        # 获取选中的一级目录名称
        first_name = request.POST.get('first_dir')
        # 获取点击的库名并转换成英文
        depart = request.POST.get('depart')
        if depart and first_name:
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
                    secondName_list.append({'second_dir': secondName, 'sedir_map': us_secondName})

            Result = result(secondName_list)
        else:
            status = 500
            data = "传参有误"
            Result = result3(data, status)

    else:
        status = 404
        data = "该请求方式为POST请求"
        Result = result3(data, status)

    return JsonResponse(Result)


# 获取三级目录信息
def get_thirddir(request):
    if request.method == "POST":
        secondList = []
        secondName_list = []
        # 获取选中的二级目录
        second_name = request.POST.get('second_dir')
        # 获取点击的库名并转换成英文
        depart = request.POST.get('depart')
        if depart and second_name:
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
                    secondName_list.append({'third_dir': thirdName, 'thdir_map': us_thirdName})

            Result = result(secondName_list)
        else:
            status = 500
            data = "传参有误"
            Result = result3(data, status)

    else:
        status = 404
        data = "该请求方式为POST请求"
        Result = result3(data, status)

    return JsonResponse(Result)


# 获取全部部门信息
def get_toldp(request):

    if request.method == "GET":
        data = []
        db = con('test')
        cursor = db.cursor()
        sql = """select dataname from department;"""
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        total_dep = cursor.fetchall()
        for to_de in total_dep:
            print(to_de[0])
            data.append(to_de[0])
        Result = result(data)
    else:
        status = 404
        data = "该请求方式为GET请求"
        Result = result3(data, status)

    return JsonResponse(Result)


# 获取国家部门信息
def get_coundp(request):

    if request.method == "GET":
        data = []
        db = con('test')
        cursor = db.cursor()
        sql = """select dataname from department where dataname like '国%';"""
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        total_dep = cursor.fetchall()
        for to_de in total_dep:
            print(to_de[0])
            data.append(to_de[0])
        Result = result(data)
    else:
        status = 404
        data = "该请求方式为GET请求"
        Result = result3(data, status)

    return JsonResponse(Result)


# 获取省直部门信息
def get_prodp(request):

    if request.method == "GET":
        data = []
        db = con('test')
        cursor = db.cursor()
        sql = """select dataname from department where dataname like '贵州省%';"""
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        total_dep = cursor.fetchall()
        for to_de in total_dep:
            print(to_de[0])
            data.append(to_de[0])
        Result = result(data)
    else:
        status = 404
        data = "该请求方式为GET请求"
        Result = result3(data, status)

    return JsonResponse(Result)

# 获取市州部门信息
def get_citydp(request):

    if request.method == "GET":
        data = []
        db = con('test')
        cursor = db.cursor()
        sql = """select dataname from department where dataname like '%市%';"""
        print(sql)
        sql_ending = sql.encode(encoding="utf8")
        cursor.execute(sql_ending)
        total_dep = cursor.fetchall()
        for to_de in total_dep:
            print(to_de[0])
            data.append(to_de[0])
        Result = result(data)
    else:
        status = 404
        data = "该请求方式为GET请求"
        Result = result3(data, status)

    return JsonResponse(Result)


# 配置日志管理
def conf_log(request):

    if request.method == "POST":
        depart = request.POST.get('depart')
        page = request.POST.get('page_num')
        each = request.POST.get('each_num')
        if depart:
            dep_name = getPinyin(depart) # --数据库
            table_name = "mylog" # --数据表
            # page = page  # -- 第几页
            # depart = request.POST.get('depart')  # --部门
            each = each # -- 每页显示几条
            # search = request.POST.get('search') # --搜索标识
            # table_keys = request.POST.get('table_keys')  # --搜索值
            page_nation_vue(dep_name,table_name,page,depart)
    else:
        status = 404
        data = "该请求方式为GET请求"
        Result = result3(data, status)

    return JsonResponse(Result)



# 查询已发布数据接口
def getDone_interface(request):

    if request.method == "POST":
        depart = request.POST.get('depart')
        region = request.POST.get('region')
        conditionPa = request.POST.get('conditionPa')
        conditionSo = request.POST.get('conditionSo')
        page = request.POST.get('pageNumber')
        each = request.POST.get('pageSize')


        data = [{
            "interfaceName": "数据接口名称",
            "resourceId": "资源ID",
            "resourceName": "资源名称",
            "resourceDescribe":"资源描述",
            "interfaceAddress":"数据接口地址",
            "callTimes":"被调用次数"
        }]
        page = {
            "pageNumber": 1,
            "pageSize": 10,
            "totalCount": 100
        }

        Result = result1(data, page)
    else:
        status = 404
        data = "该请求方式为GET请求"
        Result = result3(data, status)

    return JsonResponse(Result)


# 查询未发布数据接口
def getUnpublished_interface(request):

    if request.method == "POST":
        depart = request.POST.get('depart')
        region = request.POST.get('region')
        conditionPa = request.POST.get('conditionPa')
        conditionSo = request.POST.get('conditionSo')
        isEncap = request.POST.get('isEncap')
        page = request.POST.get('pageNumber')
        each = request.POST.get('pageSize')


        data = [{
            "resourceId": "资源ID",
            "resourceName": "资源名称",
            "resourceDescribe":"资源描述",
            "applyNum":"申请单号",
            "applyDay":"申请日期",
            "Status":"申请状态"
        }]
        page = {
            "pageNumber": 1,
            "pageSize": 10,
            "totalCount": 100
        }

        Result = result1(data, page)
    else:
        status = 404
        data = "该请求方式为GET请求"
        Result = result3(data, status)

    return JsonResponse(Result)


