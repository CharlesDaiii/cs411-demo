from flask import render_template, request, jsonify
from flask import request, redirect, url_for
from app import app
from app import database as db_helper
from app import user_mysql as user_db
from app import user_dao

@app.route("/update/<string:ticker>/<string:account>", methods=['POST'])
def update(account, ticker):
    value = request.form['value']
    db_helper.update_sentiment(ticker, value)
    return redirect(url_for('success', name = account))

@app.route("/delete/<string:ticker>/<string:account>", methods=['POST'])
def delete(account, ticker):
    """ recieved post requests for entry delete """
    db_helper.remove_stock_by_ticker(ticker, account)
    return redirect(url_for('success', name = account))

@app.route('/search', methods= ['POST'])
def search():
    name = request.form['ticker']
    n = db_helper.getName(name)
    return render_template('Friend.html', account = n, user = name, items=db_helper.query_name(name))

@app.route('/advanced',methods= ['POST'])
def advanced():
    return render_template("advanced.html", items = db_helper.advanced())

@app.route("/create/<string:account>", methods=['POST'])
def create(account):
    """ receives post requests to add new stock """
    ticker = request.form['ticker']
    db_helper.insert_new_stock(ticker,account)
    return redirect(url_for('success', name = account))

@app.route("/")
def homepage():
  return render_template("login.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if(request.form['behave'] == 'login'):
            flag = user_dao.login_dao(request.form['name'], request.form['password'])
            print(flag)
            if flag == 1:
                return redirect(url_for('success', name=request.form['name']))
            else:
                return redirect(url_for(endpoint='fail', msg=flag))
        if(request.form['behave'] == 'register'):
            return redirect(url_for('register'))
    else:
        return render_template('404.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == 'POST':
        account = request.form['account']
        email = request.form['Email']
        firstName = request.form['FirstName']
        lastName = request.form['LastName']
        gender = request.form['Gender']
        password = request.form['password']
        user_db.register(account, email, firstName, lastName, gender, password)
        return redirect(url_for('success', name=request.form['account']))
    else:
        return render_template('404.html')

def success(name):
    n = db_helper.getName(name)
    return render_template('Index.html', account = n, user = name, items=db_helper.query_name(name))
app.add_url_rule(rule='/success/<name>', view_func=success)

@app.route('/fail/<msg>')
def fail(msg):
    return "<font color='red'>登陆失败：  %s</font>" % msg



