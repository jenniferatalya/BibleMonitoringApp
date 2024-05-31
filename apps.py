import hashlib
from functools import wraps
from flask import Flask, session, redirect, render_template, request, jsonify
from models.admin import Admin

app = Flask(__name__)
app.secret_key = '0718dc97689e5d255508a53ea5af7b57'

def auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login')
        kwargs.update(session)
        return f(*args, **kwargs)
    return decorated_function

@app.errorhandler(404)
def page_not_found(e):
    return render_template("notfound.html")

@app.errorhandler(500)
def error(e):
    return render_template("error.html")

@app.errorhandler(403)
def forbidden(e):
    return render_template("forbidden.html")

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    respone = None
    if request.method == 'GET':
        respone = render_template('login.html')
    else:
        respone = {'status': False, 'msg': 'Internal server error!', 'code': 500}
        username = request.form.get('username', '')
        rawPassword = request.form.get('password', '')
        admin = Admin()

        if username and rawPassword:
            password = hashlib.md5(rawPassword.encode()).hexdigest()
            response = admin.check_credential(username, password)
            if response['status'] and response['data'] != {}:
                session['username'] = username
                session['name'] = response['data']['admin_name']
                session['phonenumber'] = response['data']['phone']
                # session['group'] = response['data']['id_group']
                respone = redirect('/')
            else:
                respone['msg'] = 'Wrong username or password!'
                respone['code'] = 401       
                respone = render_template('login.html', **respone)
        else:
            respone['msg'] = 'Wrong username/password'
            respone['code'] = 401       
            respone = render_template('login.html', **respone)
    return respone

@app.route('/logout')
@auth
def logout(*args, **kwargs):
    session.clear()
    return redirect('/')