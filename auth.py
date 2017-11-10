from flask import Blueprint, redirect, render_template, request, url_for
import database
import app
from app import login_manager, bcrypt
from flask_login import login_user, current_user

authentication = Blueprint('authentication', __name__, template_folder = 'templates')

# login page
@authentication.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('file_routes.home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = database.find_user_by_name(username)
        if user is not None and bcrypt.check_password_hash(user.hashed_password, password) and user.is_active:
            login_user(user, remember = False)
            # go to the editor screen
            return redirect('/')

    return render_template('login.html')

# registration page for new users
@authentication.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('file_routes.home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        database.add_user(username, email, bcrypt.generate_password_hash(password, rounds = 12))
        return redirect('/login')

    return render_template('register.html')

# if there isn't proper authorization, go to the login page
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

# loads a user when they are logged in 
@login_manager.user_loader
def load_user(id):
    user = database.find_user_by_id(int(id))
    if user is not None and user.is_active:
        return user
    else:
        return None