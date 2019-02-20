# -*- coding: utf-8 -*
import subprocess
# 连接远程数据库
import pymysql
from django.http import JsonResponse


def db_con():
    sub_obj = subprocess.Popen(['mysql',
                               '-h127.0.0.1',
                               '-uroot',
                               '-proot'],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE)
    return sub_obj


# 操作日志传输
def send_log(data):
    try:
        sendLog = subprocess.Popen([
            'curl',
            '-X',
            'POST',
            'http://config:248eb62a49384a9ab0f3d251a459c9c9@1.255.1.160:17010/zato/pubsub/topic/config/',
            '-d',
            data],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        return sendLog
    except:
        return JsonResponse({'result': 1})


# 数据库连接
def con(us_china):
    print(us_china, '连接数据库')
    db = pymysql.connect('127.0.0.1',
                         'root',
                         'root',
                         us_china,
                         charset='utf8')
    return db


# 中间库连接
def middle_con(dab):
    print(dab, '中间库连接')
    db = pymysql.connect('192.168.41.92',
                         'dispatchGLA',
                         'DispatchGLA',
                         dab,
                         charset='utf8')
    return db


def sub_sql(us_china):
    sql = "mysql -uroot -proot {0} < ./sql_config/test11.sql".format(us_china)
    return sql


# 获取状态日志
def get_status():
    statusLog = subprocess.Popen([
        'curl',
        '-XPOST',
        '-H',
        'X-Zato-PubSub-Key:K04MH6GYG31J6W7AFHA2VEBYVRAM',
        'http://user:123456@1.255.1.160:11223/zato/pubsub/msg/yanglao/',
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    return statusLog


# 将状态日志存到stalog表中
#def input_status(data):
#    db = con('test')
#    sql = """insert into stalog values {0};""".format(data)
#    print(sql)
#    sql_ending = sql.encode(encoding="utf8")
#    cursor.execute(sql_ending)
#    db.commit()
#    db.close()
