from flask import render_template
from flask import request, redirect, url_for, jsonify
from app import app
from app import database as db_helper
from app import user_mysql as user_db
from app import user_dao

@app.route("/edit/<int:task_id>", methods=['POST'])
def update(task_id):
    """ recieved post requests for entry updates """

    data = request.get_json()

    try:
        if "status" in data:
            db_helper.update_status_entry(task_id, data["status"])
            result = {'success': True, 'response': 'Status Updated'}
        elif "description" in data:
            db_helper.update_task_entry(task_id, data["description"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/delete/<string:symbol>/<string:account>", methods=['POST'])
def delete(account, symbol):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_task(account, symbol)
        return redirect(url_for('success', name=account))
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    print(data)
    db_helper.insert_new_task(data['description'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/")
def homepage():
  return render_template("login.html")



@app.route('/login', methods=['POST', 'GET'])
def login():
    print(request.method)
    if request.method == 'POST':
        print(request.form)
        if(request.form['behave'] == 'Change Password'):
            return redirect(url_for('update_password'))
        if(request.form['behave']=='logout'):
            return render_template("login.html")
        if(request.form['behave'] == 'login'):
            print(request.form)
            flag = user_dao.login_dao(request.form['name'], request.form['password'])
            print(flag)
            if flag == 1:
                return redirect(url_for('success', name=request.form['name']))
            else:
                return redirect(url_for(endpoint='fail', msg=flag))
        if(request.form['behave'] == 'register'):
            return redirect(url_for('register'))
    else:
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

@app.route('/search', methods=['POST', 'GET'])
def search():
    symbol = request.form['search']
    items,pop_items =db_helper.search_stock(symbol)
    return render_template("search.html", items = items, pop_items = pop_items)


def success(name):
    n = db_helper.getName(name)
    return render_template('index.html', account = n, items=db_helper.query_name(name), account_name = name)
app.add_url_rule(rule='/success/<name>', view_func=success)
#app.add_url_rule(rule='/search/<name>',  view_func=search)
@app.route('/fail/<msg>')
def fail(msg):
    return "<font color='red'>Log in failed：  %s</font>" % msg



