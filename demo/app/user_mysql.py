import pymysql

def get_by_name(account):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='mouse010311', database='mydatabase', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from LoginInfo where account='%s'" % account
    # sql = "select * from user"
    cursor.execute(sql)
    results = format_data(cursor.description, cursor.fetchall())
    cursor.close()
    conn.close()
    return results

def register(account, email, firstName, lastName, gender, password):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='mouse010311', database='mydatabase', charset='utf8')
    cursor = conn.cursor()
    sql = "insert into User values('%s','%s','%s','%s','%s')" % (account, firstName, lastName, email, gender)
    cursor.execute(sql)
    sql = "insert into LoginInfo values('%s','%s','%s')" % (account, password ,email)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def update_account(account, old_password, new_password):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='mouse010311', database='mydatabase', charset='utf8')
    cur = conn.cursor()
    sql = "select password from LoginInfo where account = '%s'" %(account)
    cur.execute(sql)
    match = cur.fetchall()[0][0] == old_password
    if(not match):
        cur.close()
        conn.close()
        return False
    sql = "update  LoginInfo set Password = '%s' where account = '%s'"  %(new_password, account)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return True

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
