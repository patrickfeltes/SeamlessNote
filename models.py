# All database models will be in this file

from app import db

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