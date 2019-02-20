# -*- coding: utf-8 -*
from uti.db_connect import con


def get_num(data):
    # 用户接口数计算
    db = con('test')
    cursor = db.cursor()
    sql = """select count(*) from Uuser where depart = '{0}';""".format(data)
    print(sql)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    user_num = cursor.fetchall()[0][0]
    print(user_num,"+"*100)

    sql = """select dataname from department where us_dataname = '{0}';""".format(data)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    departName = cursor.fetchall()[0][0]
    print(departName)
    db.close()
    # 数据目录接口数计算
    db = con(data)
    cursor = db.cursor()
    sql = """select count(*) from Uservice;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    service_num = cursor.fetchall()[0][0]
    print(service_num)
    # 访问控制接口数计算
    sql = """select count(*) from Uacl;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    acl_num = cursor.fetchall()[0][0]
    print(acl_num)
    # 流量控制接口数计算
    sql = """select count(*) from Ucontrols;"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    controls_num = cursor.fetchall()[0][0]
    print(controls_num)
    # 安全目录接口总数
    safe_num = acl_num+controls_num
    # 数据库桥接接口数计算
    sql = """select count(*) from dbList"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    dbList_num = cursor.fetchall()[0][0]
    print(dbList_num)
    # 文件接口数计算
    sql = """select count(*) from fileList"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    fileList_num = cursor.fetchall()[0][0]
    print(fileList_num)
    # 接口数数量计算
    sql = """select count(*) from interfaceList"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    interfaceList_num = cursor.fetchall()[0][0]
    print(interfaceList_num)
    # 信息接口数计算
    sql = """select count(*) from messageList"""
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    messageList_num = cursor.fetchall()[0][0]
    print(messageList_num)
    # 数据桥接接口总数
    data_num = dbList_num+fileList_num+interfaceList_num+messageList_num
    db.close()
    # 超管总接口数
    total_num = user_num+service_num+safe_num+data_num
    get_number = {'departname': departName,
                    'user_num': user_num,
                    'service_num': service_num,
                    'acl_num': acl_num,
                    'controls_num': controls_num,
                    'dbList_num': dbList_num,
                    'fileList_num': fileList_num,
                    'interfaceList_num': interfaceList_num,
                    'messageList_num': messageList_num,
                    'safe_num': safe_num,
                    'data_num': data_num,
                    'total_num': total_num
                    }

    return get_number





