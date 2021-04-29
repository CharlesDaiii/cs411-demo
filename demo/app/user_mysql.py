# import pymysql
from app import db

def connectSQL():
	conn = db.connect()
	return conn

def get_by_name(account):
    conn = connectSQL()
    sql = "select * from LoginInfo where account='%s'" % account
    # sql = "select * from user"
    results = conn.execute(sql)
    results = format_data(results.fetchall())
    conn.close()
    return results

def register(account, email, firstName, lastName, gender, password):
    conn = connectSQL()
    sql = "insert into User values('%s','%s','%s','%s','%s')" % (account, firstName, lastName, email, gender)
    conn.execute(sql)
    sql = "insert into LoginInfo values('%s','%s','%s')" % (account, password ,email)
    conn.execute(sql)
    # conn.commit()
    conn.close()

def update_account(account, old_password, new_password):
    conn = connectSQL()
    sql = "select password from LoginInfo where account = '%s'" %(account)
    results = conn.execute(sql)
    match = results.fetchall()[0][0] == old_password
    if(not match):
        conn.close()
        return False
    sql = "update  LoginInfo set Password = '%s' where account = '%s'"  %(new_password, account)
    conn.execute(sql)
    # conn.commit()
    conn.close()
    return True

def format_data(result):
    list = []
    for i in result:
        item = {
			"account":i[0],
			"Password":i[1],
			"Email":i[2]
		}
        list.append(item)
    return list
