from flask import Flask, request, render_template
import pymysql
pymysql.install_as_MySQLdb()
from flask_sqlalchemy import SQLAlchemy
from secrets import DB_NAME, DB_USERNAME, DB_PASSWORD

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
    return User.query.filter_by(username=name).first().id

# adds a new note to the database corresponding to the current user
def add_new_note(filename, file_contents, username):
    note = Note(filename, file_contents, find_user_id_by_name(username))
    db.session.add(note)
    db.session.commit()

# User model for the users table
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    hashed_password = db.Column(db.String(100), unique=False)

    def __init__(self, username, email, hashed_password):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password

    def __repr__(self):
        return 'User: ' + self.username

# Note model for the notes table
class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), unique=True)
    file_contents = db.Column(db.String(20000), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, filename, file_contents, user_id):
        self.filename = filename
        self.file_contents = file_contents
        self.user_id = user_id

    def __repr__(self):
        return 'Note: ' + self.filename


# will run twice if debug is set to True
if __name__ == '__main__':
    app.run(debug = True)