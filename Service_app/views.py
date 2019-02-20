from django.shortcuts import render
from uti.db_connect import con
from django.http import JsonResponse
# Create your views here.
def serviceFind(request, args=None):
    db = con('Service_dic')
    cursor = db.cursor()
    if args is None:
        sql = """select * from servicedata """
        sql_ending = sql.encode(encoding="utf8")
        # print(sql)
        cursor.execute(sql_ending)
        services = cursor.fetchall()
        return JsonResponse({'result':services})
    else:
        sql = """select * from servicedata where  link_name ='{0}'; """.format(args)
        sql_ending = sql.encode(encoding="utf8")
        # print(sql)
        cursor.execute(sql_ending)
        services = cursor.fetchall()
        return JsonResponse({'result': services})