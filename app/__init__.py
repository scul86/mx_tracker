from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
#from .auth import auth as auth_blueprint
#from config import config

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
#app.register_blueprint(auth_blueprint)
bootstrap.init_app(app)
login_manager.init_app(app)

from app import views, models