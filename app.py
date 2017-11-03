from flask import Flask, request, render_template, flash, redirect
import pymysql
pymysql.install_as_MySQLdb()
from flask_sqlalchemy import SQLAlchemy
from secrets import DB_NAME, DB_USERNAME, DB_PASSWORD

from flask_login import LoginManager
from flask_login import *
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@localhost/' + DB_NAME
# This option has a high overhead if enabled. Only use if necessary
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['TESTING'] = False

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

import models
import database_utils

@app.route('/')
@login_required
def home():
    return render_template('editor.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = database_utils.find_user_by_name(db, username)
        if user is not None and bcrypt.check_password_hash(user.hashed_password, password) and user.is_active:
            login_user(user, remember = False)
            # go to the editor screen
            return redirect('/')

        
    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = models.User(username, email, bcrypt.generate_password_hash(password, rounds = 12))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')


# saves a file to the database and returns the filename and contents
@app.route('/save', methods = ['GET', 'POST'])
@login_required
def save():
    file_name = ''
    file_contents = ''
    if request.method == 'POST':
        file_name = request.form['filename_field']
        file_contents = request.form['editor']
    else:
        file_name = request.args.get('filename_field')
        file_contents = request.args.get('editor')
    database_utils.add_new_note(db, file_name, file_contents, current_user.username)
    return file_name + file_contents

# if there isn't proper authorization, go to the login page
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

@login_manager.user_loader
def load_user(id):
    user = database_utils.find_user_by_id(db, int(id))
    if user is not None and user.is_active:
        return user
    else:
        return None

# will run twice if debug is set to True
if __name__ == '__main__':
    app.run(debug = True)