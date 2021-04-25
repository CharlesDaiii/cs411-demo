import random
import pymysql


def query_name(account):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456.', database='whatsup', charset='utf8')
    cursor = conn.cursor()
    sql = "Select s.ticker, s.overall, s.positive, s.negative From Sentiment s join Pick p On s.ticker = p.stock Where p.user = '%s' order by s.overall desc" % account
    cursor.execute(sql)
    results = format_data(cursor.description, cursor.fetchall())
    cursor.close()
    conn.close()
    return results


def update_sentiment(ticker, value):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456.', database='whatsup', charset='utf8')
    cursor = conn.cursor()
    sql = "UPDATE Sentiment SET overall = '{value}' where ticker = '{ticker}'; ".format(ticker=ticker, value=value)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def format_data(fields, results):
    list = []
    for i in results:
        item = {
            "ticker": i[0],
            "overall": i[1],
            "positive": i[2],
            "negative": i[3]
        }
        list.append(item)
    return list


def getName(account):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456.', database='whatsup', charset='utf8')
    cur = conn.cursor()

    sql = "select * from User where account='%s'" % account
    cur.execute(sql)
    userinfo = cur.fetchall()
    print(userinfo)
    name = userinfo[0][1] + " " + userinfo[0][2]
    cur.close()
    conn.close()
    return name


def advanced():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456.', database='whatsup', charset='utf8')
    cursor = conn.cursor()
    sql = "Select u1.FirstName, u1.LastName, avg(s1.overall) as sentiment_score From Sentiment s1 join Pick p1 on s1.ticker = p1.stock join User u1 on u1.account = p1.user Group by u1.account Order by sentiment_score desc Limit 15;"
    cursor.execute(sql)
    results = format_advanced_data(cursor.description, cursor.fetchall())
    cursor.close()
    conn.close()
    return results


def format_advanced_data(fields, results):
    list = []
    for i in results:
        item = {
            "category": i[0],
            "output": i[1],
        }
        list.append(item)
    return list


def insert_new_stock(ticker: str, account: str) -> int:
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456.', database='whatsup', charset='utf8')
    cursor = conn.cursor()
    query = 'Insert Into Pick (user, stock) VALUES ("{}", "{}");'.format(account, ticker)
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


def remove_stock_by_ticker(ticker: str, account: int) -> None:
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456.', database='whatsup', charset='utf8')
    cursor = conn.cursor()
    sql = "Delete from Pick where stock = '{ticker}' and user = '{account}'".format(ticker=ticker, account=account)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()