from flask import render_template
from flask import request, redirect, url_for
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

@app.route("/delete/<int:task_id>", methods=['POST'])
def delete(task_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_task_by_id(task_id)
        result = {'success': True, 'response': 'Removed task'}
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
    return render_template('index.html', account = n, items=db_helper.query_name(name))
app.add_url_rule(rule='/success/<name>', view_func=success)

@app.route('/fail/<msg>')
def fail(msg):
    return "<font color='red'>登陆失败：  %s</font>" % msg



