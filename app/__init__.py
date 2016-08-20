from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from decimal import *

import pickle
# from config import config


def set_pickled_decimal(num):
    float(num) # This just makes sure the param is a number
    return pickle.dumps(Decimal(num))


def add_pickled_data(a, b):
    return pickle.dumps(pickle.loads(a) + pickle.loads(b))

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bootstrap.init_app(app)
login_manager.init_app(app)

from .auth import auth as auth_blueprint # This call needs to be after creation of 'db' variable
app.register_blueprint(auth_blueprint)

from app import views, models