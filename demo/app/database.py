import random
import pymysql


def query_name(account):
	conn = pymysql.connect(host='127.0.0.1', user='root', password='mouse010311', database='mydatabase', charset='utf8')
	cursor = conn.cursor()
	sql = "select * from Pick where user='%s'" % account
	cursor.execute(sql)
	results = format_data(cursor.description, cursor.fetchall())
	cursor.close()
	conn.close()
	return results

def format_data(fields, results):
    index = 0
    list = []
    for i in results:
    	index+=1
    	item = {
    		"id":index,
    		"task":i[1],
    		"status":"Up"
    	}
    	list.append(item)
    return list
def getName(account):
	conn = pymysql.connect(host='127.0.0.1', user='root', password='mouse010311', database='mydatabase', charset='utf8')
	cur = conn.cursor()
	
	sql = "select * from User where account='%s'" % account
	cur.execute(sql)
	userinfo = cur.fetchall()
	name = userinfo[0][1] + " " + userinfo[0][2]
	print(cur.fetchall())
	cur.close()
	conn.close()
	return name

def stock_list():
	print("in stock list()")
	list = ["A", "B", "C"]
	return list

def insert_new_task(symbol):
	item = {
		"id":1,
		"task": symbol,
		"status": "Todo"
	}
	query_result.append(item)
	return True

def remove_task_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    query_result.pop(0)