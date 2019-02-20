from django.shortcuts import render
from uti.db_connect import con
from django.http import JsonResponse
# Create your views here.


def findData(request, args=None):
    db = con('Data_dic')
    cursor = db.cursor()
    if args is None:
        sql = """select * from dataname """
        sql_ending = sql.encode(encoding="utf8")
        # print(sql)
        cursor.execute(sql_ending)
        datas = cursor.fetchall()
        return JsonResponse({'result': datas})
    else:
        sql = """select * from dataname where  data_name ='{0}'; """.format(args)
        sql_ending = sql.encode(encoding="utf8")
        # print(sql)
        cursor.execute(sql_ending)
        datas = cursor.fetchall()
        return JsonResponse({'result': datas})
