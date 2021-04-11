from flask import Flask, url_for, redirect, request, render_template
import user_dao

app = Flask('__name__')

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

# @app.route('/success/<name>/<address>/<int:age>')
# def success(name, address, age):
#     return '欢迎你%s,地址：%s,年龄：%d' % (name, address, age)
app.add_url_rule(rule='/success/<name>', view_func=success)
def success(name):
    return render_template('success.html', name=name)

@app.route('/fail/<msg>')
def fail(msg):
    return "<font color='red'>登陆失败：  %s</font>" % msg

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
