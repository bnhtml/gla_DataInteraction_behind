# -*- coding: utf-8 -*
import pymysql
from uti.db_connect import con
from uti.usercode import getPinyin

def insert_log(depart,obj_name,username,starttinme,endtime,status):

    us_china= getPinyin(depart)
    db = con(us_china)
    cursor = db.cursor()
    sql = """insert into mylog values (null,"{0}",'{1}','{2}','{3}','{4}','{5}')""".format(task,obj_name,username,starttinme,endtime,status)
    print(sql,'*'*100)
    sql_ending = sql.encode(encoding="utf8")
    cursor.execute(sql_ending)
    db.commit()
    cursor.close()
    db.close()

    return True

