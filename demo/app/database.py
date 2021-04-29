import random
# import pymysql
from app import format
from app import db
import sqlalchemy


def connectSQL():
	conn = db.connect()
	return conn

def insert_new_stock(ticker: str, account: str) ->  int:
	conn = connectSQL()
	query = 'Insert Into Pick (user, stock) VALUES ("{}", "{}");'.format(
		account, ticker)	
	conn.execute(query)
	# query_results = conn.execute("Select LAST_INSERT_ID();")
	# query_results = [x for x in query_results]
	# stock_id = query_results[0][0]
	# conn.commit()
	conn.close()
	return ticker

def remove_stock_by_ticker(ticker: str, account:int) -> None:
	""" remove entries based on task ID """
	conn = connectSQL()
	query = "Delete From Pick where stock = '{ticker}' and user = '{account}';".format(ticker = ticker, account = account)
	conn.execute(query)
	# conn.commit()
	conn.close()

def query_name(account):
	conn= connectSQL()
	sql = "select *  from Pick join Stock on Pick.stock = Stock.ticker where user='%s'" % account
	results = conn.execute(sql)
	results = format.format_stock_data(results.fetchall())
	conn.close()
	return results

def getName(account):
	conn = connectSQL()
	sql = "select * from User where account='%s'" % account
	results = conn.execute(sql)
	userinfo = results.fetchall()
	name = userinfo[0][1] + " " + userinfo[0][2]
	conn.close()
	return name

def search_stock(symbol):
	conn = connectSQL()
	symbol = "%" + symbol + "%"
	sql = "select * from Company where ticker like '{}'".format(symbol)
	stmt = sqlalchemy.text(sql)
	results = conn.execute(stmt)
	results = format.format_company_data(results.fetchall())
	sql = "select * from Company c join (select p.stock, count(p.user) as cnt from Pick p join Stock s on p.stock = s.ticker where p.stock like '%s' group by p.stock order by cnt desc limit 5) as temp on c.ticker = temp.stock;" % symbol
	stmt = sqlalchemy.text(sql)
	results2 = conn.execute(stmt)
	pop_results = format.format_company_data(results2.fetchall())
	conn.close()
	return results, pop_results

def get_companyinfo(ticker:str):
	conn = connectSQL()
	sql = "select * from Company where ticker like '%s'" % ticker
	stmt = sqlalchemy.text(sql)
	results = conn.execute(stmt)
	results = format.format_company_data(results.fetchall())
	conn.close()
	return results


def remove_task(account, symbol):
	""" remove entries based on account and symbol """
	conn = connectSQL()
	sql = "delete from Pick where user = '%s' and stock = '%s'" %(account, symbol)
	conn.execute(sql)
	# conn.commit()
	conn.close()

def get_toppick():
	conn = connectSQL()
	sql = "Select s.ticker, s.company_name, count(*) as num_pick From User u join Pick p on u.account = p.user join Stock s on p.stock = s.ticker Group by s.ticker Order by num_pick desc Limit 15;"
	results = conn.execute(sql)
	results = format.format_toppick_data(results.fetchall())
	conn.close()
	return results





