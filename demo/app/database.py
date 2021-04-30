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
	sql = """select *  
	from Pick join Stock on Pick.stock = Stock.ticker
	natural join Sentiment s 
	where user='%s'
	""" % account
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

# def get_toppick():
# 	conn = connectSQL()
# 	sql = "Select s.ticker, s.company_name, count(*) as num_pick From User u join Pick p on u.account = p.user join Stock s on p.stock = s.ticker Group by s.ticker Order by num_pick desc Limit 15;"
# 	results = conn.execute(sql)
# 	results = format.format_toppick_data(results.fetchall())
# 	conn.close()
# 	return results

def get_toppick():
	conn = connectSQL()
	sql_drop = '''
	drop Procedure IF EXISTS Result;
	'''
	sql_drop2 = '''DROP TRIGGER IF EXISTS mytrigger;'''
	sql_drop3 = '''drop table IF EXISTS NewTable;'''
	sql_table = '''create table NewTable(
				category VARCHAR(70), 
				count_status VARCHAR(30),
				avg_sentiment real,
				avg_PE real,
				PRIMARY KEY (category));'''
	sql = '''
	create procedure Result() 
	begin
		DECLARE industry VARCHAR(70);
		DECLARE total_number INT;
		DECLARE status1 VARCHAR(30);
		DECLARE exit_loop BOOLEAN DEFAULT FALSE;
		DECLARE avg_sentiment REAL;
		DECLARE avg_PE REAL;
		DECLARE curr CURSOR FOR (SELECT category, count(company_name) as cnt
								FROM Company join Pick
								on Pick.stock = Company.ticker
								GROUP BY category
								having cnt < 1000);
		DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE;
		open curr;
		loop1:LOOP
			FETCH curr into industry, total_number;
			if exit_loop then leave loop1;
			end if;
			if industry = NULL THEN LEAVE loop1;
			end if;

			if total_number < 10 then set status1 = 'Not Popular';
			ELSEIF total_number  < 50 THEN SET status1 = 'Popular';
			ELSE SET status1 = 'Very Popular';
			END IF;

			SET avg_PE = (select avg(forwardPE) as output
			from Stock s join Company c on s.company_name = c.company_name
			where s.ticker not in (
				select ticker from Sentiment
				where overall > 0
			) and c.category = industry);

			SET avg_sentiment = (select avg(overall) as output
			from Sentiment s natural join Company c
			where s.ticker not in (
				select ticker from Sentiment
				where overall < 0
			) and c.category = industry);

			Insert into NewTable Values(industry, status1, avg_sentiment, avg_PE);
		END LOOP loop1;
		CLOSE curr;
	end
	'''


	sql_trigger = ''' 
	   CREATE TRIGGER mytrigger BEFORE INSERT ON  NewTable FOR EACH ROW
	   BEGIN
		  IF new.avg_PE < 0.0 then SET new.avg_PE = 0.0;
		  END IF;
		  SET new.avg_PE = ROUND(new.avg_PE, 2);
		  SET new.avg_sentiment = ROUND(new.avg_PE, 2);
	   END 
		'''

	sql1 = "call Result();"
	sql2 = '''select * from NewTable
	where category <> ''
	order by count_status desc;'''


	conn.execute(sql_drop)
	conn.execute(sql_drop2)
	conn.execute(sql_drop3)
	conn.execute(sql_table)
	conn.execute(sql_trigger)
	conn.execute(sql)
	conn.execute(sql1)
	results = conn.execute(sql2)

	
	results = format.format_toppick_data(results.fetchall())
	conn.close()
	return results





