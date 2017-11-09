from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import database

file_routes = Blueprint('file_routes', __name__, template_folder = 'templates')

# main editor page
@file_routes.route('/')
@login_required
def home():
    return render_template('editor.html')


# saves a file to the database and returns the filename and contents
@file_routes.route('/save', methods = ['GET', 'POST'])
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
    database.add_new_note(file_name, file_contents, current_user.username)
    return file_name + file_contents