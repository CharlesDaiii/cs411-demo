from flask import render_template
from flask import request, redirect, url_for
from app import app
from flask import render_template, request, jsonify
from flask import request, redirect, url_for
from app import app
from app import database as db_helper
from app import user_mysql as user_db
from app import user_dao

@app.route("/update/<string:ticker>/<string:account>", methods=['POST'])
def update(account, ticker):
    value = request.form['ticker']
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
    return render_template("advanced.html", remind = db_helper.advanced())

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
        if (request.form['behave'] == 'search account'):
            return redirect(url_for('search_account'))
        if (request.form['behave'] == 'delect account'):
            return redirect(url_for('delect_account'))
        if (request.form['behave'] == 'update_password'):
            return redirect(url_for('update_password'))
        if (request.form['behave'] == 'logout'):
            return render_template("login.html")
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

@app.route('/delect1', methods=['POST', 'GET'])
def delect_account():
    if request.method == "GET":
        return render_template("delect account.html")
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        if (not user_db.delect_account(account, password)):
            return render_template('delect account.html', remind = "wrong password")
        return render_template("login.html")
    else:
        return render_template('404.html')


@app.route('/search account', methods=['POST', 'GET'])
def search_account():
    if request.method == "GET":
        return render_template("search account.html")
    if request.method == 'POST':
        Email = request.form['Email']
        a = user_db.search_account(Email)
        if (a == ''):
            return render_template('search account.html', remind = "email not exist")
        return render_template('search account.html', remind = '%s'%a )
    else:
        return render_template('404.html')

@app.route('/update_password', methods=['POST', 'GET'])
def update_password():
    if request.method == "GET":
        return render_template("update_password.html")
    if request.method == 'POST':
        account = request.form['account']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        if (not user_db.update_account(account, old_password, new_password)):
            return render_template('update_password.html', remind = "wrong old password")
        return render_template("login.html")
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
    return render_template('index.html', account = n, items=db_helper.query_name(name))
app.add_url_rule(rule='/success/<name>', view_func=success)

@app.route('/fail/<msg>')
def fail(msg):
    return "<font color='red'>登陆失败：  %s</font>" % msg



