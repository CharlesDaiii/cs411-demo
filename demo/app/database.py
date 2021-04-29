import random
import pymysql
from app import format

def connectSQL():
	conn = pymysql.connect(host='127.0.0.1', user='root', password='mouse010311', database='mydatabase', charset='utf8')
	cursor = conn.cursor()
	return conn, cursor

def insert_new_stock(ticker: str, account: str) ->  int:
	conn, cursor = connectSQL()
	query = 'Insert Into Pick (user, stock) VALUES ("{}", "{}");'.format(
		account, ticker)	
	cursor.execute(query)
	query_results = cursor.execute("Select LAST_INSERT_ID();")
	stock_id = query_results
	conn.commit()
	cursor.close()
	conn.close()
	return ticker

def remove_stock_by_ticker(ticker: str, account:int) -> None:
	""" remove entries based on task ID """
	conn, cursor = connectSQL()
	query = "Delete From Pick where stock = '{ticker}' and user = '{account}';".format(ticker = ticker, account = account)
	cursor.execute(query)
	conn.commit()
	cursor.close()
	conn.close()

def query_name(account):
	conn, cursor = connectSQL()
	sql = "select *  from Pick join Stock on Pick.stock = Stock.ticker where user='%s'" % account
	cursor.execute(sql)
	results = format.format_stock_data(cursor.description, cursor.fetchall())
	cursor.close()
	conn.close()
	return results

def getName(account):
	conn, cur = connectSQL()
	sql = "select * from User where account='%s'" % account
	cur.execute(sql)
	userinfo = cur.fetchall()
	name = userinfo[0][1] + " " + userinfo[0][2]
	cur.close()
	conn.close()
	return name

def search_stock(symbol):
	conn, cursor = connectSQL()
	symbol = "%" + symbol + "%"
	sql = "select * from Company where ticker like '%s'" % symbol
	cursor.execute(sql)
	results = format.format_company_data(cursor.description, cursor.fetchall())
	sql = "select * from Company c join (select p.stock, count(p.user) as cnt from Pick p join Stock s on p.stock = s.ticker where p.stock like '%s' group by p.stock order by cnt desc limit 5) as temp on c.ticker = temp.stock;" % symbol
	cursor.execute(sql)
	pop_results = format.format_company_data(cursor.description, cursor.fetchall())
	cursor.close()
	conn.close()
	return results, pop_results

def get_companyinfo(ticker:str):
	conn, cursor = connectSQL()
	sql = "select * from Company where ticker like '%s'" % ticker
	cursor.execute(sql)
	results = format.format_company_data(cursor.description, cursor.fetchall())
	cursor.close()
	conn.close()
	return results


def remove_task(account, symbol):
	""" remove entries based on account and symbol """
	conn, cur = connectSQL()
	sql = "delete from Pick where user = '%s' and stock = '%s'" %(account, symbol)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()

def get_toppick():
	conn, cursor = connectSQL()
	sql = "Select s.ticker, s.company_name, count(*) as num_pick From User u join Pick p on u.account = p.user join Stock s on p.stock = s.ticker Group by s.ticker Order by num_pick desc Limit 15;"
	cursor.execute(sql)
	results = format.format_toppick_data(cursor.description, cursor.fetchall())
	cursor.close()
	conn.close()
	return results





