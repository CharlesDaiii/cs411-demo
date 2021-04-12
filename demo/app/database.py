import random
import pymysql


def query_name(account):
	conn = pymysql.connect(host='127.0.0.1', user='root', password='mouse010311', database='mydatabase', charset='utf8')
	cursor = conn.cursor()
	sql = "select stock from Pick where user='%s'" % account
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
    		"symbol":i[0],
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
	cur.close()
	conn.close()
	return name

def search_stock(symbol):
	conn = pymysql.connect(host='127.0.0.1', user='root', password='mouse010311', database='mydatabase', charset='utf8')
	cursor = conn.cursor()
	symbol = "%" + symbol + "%"
	sql = "select * from Stock where ticker like '%s'" % symbol
	cursor.execute(sql)
	results = format_data(cursor.description, cursor.fetchall())

	sql = "select p.stock, count(p.user) as cnt from Pick p join Stock s on p.stock = s.ticker where p.stock like '%s' group by p.stock order by cnt desc limit 5;" % symbol
	cursor.execute(sql)
	pop_results = format_data(cursor.description, cursor.fetchall())
	cursor.close()
	conn.close()
	return results, pop_results

def insert_new_task(symbol):
	item = {
		"id":1,
		"task": symbol,
		"status": "Todo"
	}
	query_result.append(item)
	return True

def remove_task(account, symbol):
	""" remove entries based on account and symbol """
	conn = pymysql.connect(host='127.0.0.1', user='root', password='mouse010311', database='mydatabase', charset='utf8')
	cur = conn.cursor()
	sql = "delete from Pick where user = '%s' and stock = '%s'" %(account, symbol)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()




