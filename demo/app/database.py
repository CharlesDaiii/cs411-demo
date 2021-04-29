import random
# import pymysql
from app import db




def update_stock_info(ticker: str, customized_name: str):
	# conn = pymysql.connect(host='127.0.0.1', user='root', password='Hjl200807', database='whatsup', charset='utf8')
	conn = db.connect()
	cursor = conn.cursor()
	sql = "Update Stock set company_name = '{}' where ticker = '{}';".format(customized_name, ticker)
	# print(sql)
	cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()


def get_toppick():
	# conn = pymysql.connect(host='127.0.0.1', user='root', password='Hjl200807', database='whatsup', charset='utf8')
	conn = db.connect()
	cursor = conn.cursor()
	sql = "Select s.ticker, s.company_name, count(*) as num_pick From User u join Pick p on u.account = p.user join Stock s on p.stock = s.ticker Group by s.ticker Order by num_pick desc Limit 15;"
	cursor.execute(sql)
	results = format_toppick_data(cursor.description, cursor.fetchall())
	cursor.close()
	conn.close()
	return results

def format_toppick_data(fields, results):
	list = []
	for i in results:
		item = {
			"ticker":i[0],
			"company_name":i[1],
			"num_pick":i[2]
		}
		list.append(item)
	return list

def get_companyinfo(ticker:str):
	# conn = pymysql.connect(host='127.0.0.1', user='root', password='Hjl200807', database='whatsup', charset='utf8')
	conn = db.connect()
	cursor = conn.cursor()
	sql = "select *  from Company where ticker='{}'".format(ticker)
	cursor.execute(sql)
	results = format_company_data(cursor.description, cursor.fetchall())
	cursor.close()
	conn.close()
	return results

def format_company_data(fields, results):
	list = []
	for i in results:
		item = {
			"ticker":i[0],
			"company_name":i[1],
			"category":i[2],
			"region":i[3],
			"CEO_Name":i[4]
		}
		list.append(item)
	return list

def query_name(account):
	# conn = pymysql.connect(host='127.0.0.1', user='root', password='Hjl200807', database='whatsup', charset='utf8')
	conn = db.connect()
	# cursor = conn.cursor()
	sql = "select *  from Pick join Stock on Pick.stock = Stock.ticker where user='%s'" % account
	results = conn.execute(sql)
	results = format_stock_data(results.fetchall())
	# cursor.close()
	conn.close()
	return results

def format_stock_data(results):
	index = 0
	list = []
	for i in results:
		index+=1
		item = {
			"id":index,
			"ticker":i[1],
			"company_name":i[3],
			"fiftyTwoWeekLow":i[4],
			"fiftyTwoWeekHigh":i[5],
			"forwardPE":i[6],
			"trailingPE":i[7]
		}
		list.append(item)
	return list
def getName(account):
	# conn = pymysql.connect(host='127.0.0.1', user='root', password='Hjl200807', database='whatsup', charset='utf8')
	conn = db.connect()
	# cur = conn.cursor()
	
	sql = "select * from User where account='%s'" % account
	results = conn.execute(sql)
	userinfo = results.fetchall()
	name = userinfo[0][1] + " " + userinfo[0][2]
	# print(cur.fetchall())
	# cur.close()
	conn.close()
	return name


def insert_new_stock(ticker: str, account: str) ->  int:
	# conn = pymysql.connect(host='127.0.0.1', user='root', password='Hjl200807', database='whatsup', charset='utf8')
	conn = db.connect()
	cursor = conn.cursor()
	query = 'Insert Into Pick (user, stock) VALUES ("{}", "{}");'.format(
		account, ticker)	
	cursor.execute(query)
	query_results = cursor.execute("Select LAST_INSERT_ID();")
	stock_id = query_results
	conn.commit()
	cursor.close()
	conn.close()

	return stock_id

# def update_task_entry(stock_id: int, ticker: str) -> None:
#     """Updates task description based on given `task_id`

#     Args:
#         task_id (int): Targeted task_id
#         text (str): Updated description

#     Returns:
#         None
#     """

#     conn = pymysql.connect(host='127.0.0.1', user='root', password='Hjl200807', database='whatsup', charset='utf8')
# 	cursor = conn.cursor()
#     query = 'Update Pick set task = "{}" where id = {};'.format(text, task_id)
#     cursor.execute(query)
# 	conn.commit()
# 	cursor.close()
#     conn.close()



# def name_to_account(name):
# 	first_name = name.split(" ")[0]
# 	last_name = name.split(" ")[1]
# 	conn = pymysql.connect(host='127.0.0.1', user='root', password='Hjl200807', database='whatsup', charset='utf8')
# 	cursor = conn.cursor()
# 	query = "Select ticker from User where FirstName = {first_name} and LastName - {last_name}".format(first_name = first_name, last_name = last_name)
# 	cursor.execute(query)
# 	cursor.close()
# 	conn.close()

def remove_stock_by_ticker(ticker: str, account:int) -> None:
	""" remove entries based on task ID """
	# conn = pymysql.connect(host='127.0.0.1', user='root', password='Hjl200807', database='whatsup', charset='utf8')
	conn = db.connect()
	cursor = conn.cursor()
	query = "Delete From Pick where stock = '{ticker}' and user = '{account}';".format(ticker = ticker, account = account)
	cursor.execute(query)
	conn.commit()
	cursor.close()
	conn.close()