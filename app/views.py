from app import app
from flask_login import login_required

@app.route('/')
@app.route('/index')
def index():
    return '<h1> Hello World</h1>'

@app.route('/user/<name>')
#@login_required
def user(name):
    return '<h1>Hello, {}</h1>'.format(name)