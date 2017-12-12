from flask import Flask
import pymysql
pymysql.install_as_MySQLdb()
from flask_sqlalchemy import SQLAlchemy
from secrets import DB_NAME, DB_USERNAME, DB_PASSWORD

from flask_login import *
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@localhost/' + DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# this will actually be secret in production
app.config['SECRET_KEY'] = 'dev'
app.config['TESTING'] = False

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)