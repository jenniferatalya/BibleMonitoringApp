import api
from apps import app, auth, render_template

@app.route('/')
@auth
def dashboard(*args, **kwargs):
    return render_template('dashboard.html', **kwargs)

@app.route('/report')
@auth
def report(*args, **kwargs):
    return render_template('report.html', **kwargs)

@app.route('/devotion')
@auth
def devotion(*args, **kwargs):
    return render_template('devotion.html', **kwargs)

@app.route('/member')
@auth
def member(*args, **kwargs):
    return render_template('member.html', **kwargs)

@app.route('/group')
@auth
def group(*args, **kwargs):
    return render_template('group.html', **kwargs)

@app.route('/church')
@auth
def church(*args, **kwargs):
    return render_template('church.html', **kwargs)

@app.route('/admin')
@auth
def admin(*args, **kwargs):
    return render_template('admin.html', **kwargs)

if __name__ == '__main__':

    app.run(debug=True, port=8080)