from flask import render_template
from flask import request, redirect, url_for, jsonify
from app import app
from app import database as db_helper
from app import user_mysql as user_db
from app import user_dao


@app.route("/")
def homepage():
  return render_template("login.html")

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

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print(request.form)
        if(request.form['behave'] == 'Change Password'):
            return redirect(url_for('update_password'))
        if(request.form['behave']=='logout'):
            return render_template("login.html")
        if(request.form['behave'] == 'login'):
            flag = user_dao.login_dao(request.form['name'], request.form['password'])
            if flag == 1:
                return redirect(url_for('success', name=request.form['name']))
            else:
                return redirect(url_for(endpoint='fail', msg=flag))
        if(request.form['behave'] == 'register'):
            return redirect(url_for('register'))
    else:
        return render_template("login.html")

def success(name):
    n = db_helper.getName(name)
    return render_template('index.html', account = n, user = name, items=db_helper.query_name(name))
app.add_url_rule(rule='/success/<name>', view_func=success)

@app.route('/search/<string:name>', methods= ['POST'])
def search(name):
    print()
    if('behave' in request.form):
        if(request.form['behave'] == 'back'):
            return redirect(url_for('success', name=name))
    ticker = request.form['ticker']
    items,pop_items =db_helper.search_stock(ticker)
    return render_template("search.html", items = items, pop_items = pop_items, user = name)
app.add_url_rule(rule='/search/<name>', view_func=search)


@app.route("/create/<string:account>", methods=['POST'])
def create(account):
    """ receives post requests to add new stock """
    ticker = request.form['ticker']
    db_helper.insert_new_stock(ticker,account)
    return redirect(url_for('success', name = account))

@app.route("/update/<string:account>/<string:ticker>", methods=['POST'])
def update(ticker,account):
    name = request.form['company_name']
    db_helper.update_stock_info(ticker,name)
    return redirect(url_for('success', name = account))

@app.route("/delete/<string:ticker>/<string:account>", methods=['POST'])
def delete(account,ticker):
    """ recieved post requests for entry delete """
    try:
        db_helper.remove_stock_by_ticker(ticker,account)
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    return redirect(url_for('success', name = account))


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

# @app.route('/search', methods=['POST', 'GET'])
# def search():
#     symbol = request.form['search']
#     items,pop_items =db_helper.search_stock(symbol)
#     return render_template("search.html", items = items, pop_items = pop_items)

@app.route('/top_pick',methods= ['POST'])
def top_pick():
    return render_template("top_pick.html", items = db_helper.get_toppick())



@app.route('/fail/<msg>')
def fail(msg):
    return "<font color='red'>Log in failed：  %s</font>" % msg



