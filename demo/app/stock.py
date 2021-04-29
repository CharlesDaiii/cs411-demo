# import pymysql
from app import db


def get_by_name(account):
    # conn = pymysql.connect(host='127.0.0.1', user='root', password='Hjl200807', database='whatsup', charset='utf8')
    conn = db.connect()
    cursor = conn.cursor()
    sql = "select * from Stock where account='%s'" % account
    # sql = "select * from user"
    cursor.execute(sql)
    results = format_data(cursor.description, cursor.fetchall())
    cursor.close()
    conn.close()
    return results

# 数据格式化 fields 字段名，result 结果集
def format_data(fields, result):
    # 列字段数组 格式['id', 'name', 'password']
    field = []
    for i in fields:
        field.append(i[0])
    # 返回的数组集合 格式[{'id': 1, 'name': 'admin', 'password': '123456'}]
    results = []
    for res in result:
        line_data = {}
        for index in range(0, len(field)):
            line_data[field[index]] = res[index]
        results.append(line_data)
    return results
