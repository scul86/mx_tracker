from app import app
from flask_login import login_required

@app.route('/')
@app.route('/index')
def index():
    return '<h1> Hello World</h1>'

@app.route('/vehicle/<name>')
@login_required
def vehicle(name):
    return '<h1>Hello, {}</h1>'.format(name)