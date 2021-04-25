from app import user_mysql, user_model

def login_dao(name, password):
    if len(user_mysql.get_by_name(name)) > 0:
        res = user_mysql.get_by_name(name)[0]
        user = user_model.User(name=res['account'], password=res['Password'])
        if user.name == name and user.password == password:
            return 1
        else:
            return '密码错误'
    return '用户名不存在'