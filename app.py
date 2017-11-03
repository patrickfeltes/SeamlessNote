from flask import Flask, request, render_template
import pymysql
pymysql.install_as_MySQLdb()
from flask_sqlalchemy import SQLAlchemy
from secrets import DB_NAME, DB_USERNAME, DB_PASSWORD
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@localhost/' + DB_NAME
# This option has a high overhead if enabled. Only use if necessary
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# this is temporary until we have a login system
current_username = 'username'

db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('editor.html')

# saves a file to the database and returns the filename and contents
@app.route('/save', methods = ['GET', 'POST'])
def save():
    file_name = ''
    file_contents = ''
    if request.method == 'POST':
        file_name = request.form['filename_field']
        file_contents = request.form['editor']
    else:
        file_name = request.args.get('filename_field')
        file_contents = request.args.get('editor')
    add_new_note(file_name, file_contents, current_username)
    return file_name + file_contents

# given a user name, find the unique id associated with that user
def find_user_id_by_name(name):
    return models.User.query.filter_by(username=name).first().id

def add_user(name, email, password):
    user = models.User(name, email, password)
    db.session.add(user)
    db.session.commit()

# adds a new note to the database corresponding to the current user
def add_new_note(filename, file_contents, username):
    note = models.Note(filename, file_contents, find_user_id_by_name(username))
    db.session.add(note)
    db.session.commit()

# will run twice if debug is set to True
if __name__ == '__main__':
    app.run(debug = True)