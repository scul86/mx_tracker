#!venv/bin/python3

from flask import Flask
from flask_sslify import SSLify

app = Flask(__name__)
#sslify = SSLify(app)

@app.route('/')
def index():
    return '<h1> Hello World</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}</h1>'.format(name)

if __name__ == '__main__':
    app.run(debug=False)