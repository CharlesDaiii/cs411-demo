from flask import render_template, request, jsonify
from flask import request, redirect, url_for
from app import app
from app import database as db_helper
from app import user_dao


@app.route("/update/<string:account>/<string:ticker>", methods=['POST'])
def update(ticker,account):
    name = request.form['company_name']
    db_helper.update_stock_info(ticker,name)
    return redirect(url_for('success', name = account))


# @app.route("/edit/<int:task_id>", methods=['POST'])
# def update(task_id):
#     """ recieved post requests for entry updates """

#     data = request.get_json()

#     try:
#         if "status" in data:
#             db_helper.update_status_entry(task_id, data["status"])
#             result = {'success': True, 'response': 'Status Updated'}
#         elif "description" in data:
#             db_helper.update_task_entry(task_id, data["description"])
#             result = {'success': True, 'response': 'Task Updated'}
#         else:
#             result = {'success': True, 'response': 'Nothing Updated'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     return jsonify(result)

@app.route("/delete/<string:ticker>/<string:account>", methods=['POST'])
def delete(account,ticker):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_stock_by_ticker(ticker,account)
        # result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return redirect(url_for('success', name = account))

@app.route("/create/<string:account>", methods=['POST'])
def create(account):
    """ receives post requests to add new stock """
    ticker = request.form['ticker']
    # data = request.get_json()
    # print(data)
    db_helper.insert_new_stock(ticker,account)
    # result = {'success': True, 'response': 'Done'}
    return redirect(url_for('success', name = account))
    


@app.route("/")
def homepage():
  return render_template("login.html")



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        flag = user_dao.login_dao(request.form['name'], request.form['password'])
        print(flag)
        if flag == 1:
            return redirect(url_for('success', name=request.form['name']))
        else:
            return redirect(url_for(endpoint='fail', msg=flag))
    else:
        return render_template('404.html')

def success(name):
    n = db_helper.getName(name)
    return render_template('index.html', account = n, user = name, items=db_helper.query_name(name))
app.add_url_rule(rule='/success/<name>', view_func=success)


@app.route('/search', methods= ['POST'])
def search():
    ticker = request.form['ticker']
    return render_template('company.html', stock_ticker = ticker, items=db_helper.get_companyinfo(ticker))

@app.route('/top_pick',methods= ['POST'])
def top_pick():
    return render_template("top_pick.html", items = db_helper.get_toppick())


@app.route('/fail/<msg>')
def fail(msg):
    return "<font color='red'>登陆失败：  %s</font>" % msg



