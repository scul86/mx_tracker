from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .auth import auth as auth_blueprint

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(auth_blueprint)
db = SQLAlchemy(app)

from app import views, models