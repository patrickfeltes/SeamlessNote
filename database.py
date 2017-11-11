# all database interaction is in this file
from app import db
from flask_login import UserMixin

# User model for the users table
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(120), unique = True)
    hashed_password = db.Column(db.String(100), unique = False)

    def __init__(self, username, email, hashed_password):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password

    def __repr__(self):
        return 'User: ' + self.username

# Note model for the notes table
class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(100), unique = True)
    file_contents = db.Column(db.String(20000), unique = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, filename, file_contents, user_id):
        self.filename = filename
        self.file_contents = file_contents
        self.user_id = user_id

    def __repr__(self):
        return 'Note: ' + self.filename

# Tag model for the tags table
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key = True)
    tag_name = db.Column(db.String(100), unique = True)

    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __repr__(self):
        return 'Tag: ' + self.tag_name

# NoteTagJunction model for the note_tab_junctions table
class NoteTagJunction(db.Model):
    __tablename__ = 'note_tag_junction'
    id = db.Column(db.Integer, primary_key = True)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))

    def __init__(self, note_id, tag_id):
        self.note_id = note_id
        self.tag_id = tag_id

    def __repr__(self):
        return 'NoteTagJunction: ' + self.note_id + ' ' + self.tag_id

# given a user name, find the unique id associated with that user
# if that user doesn't exist, return None
def find_user_id_by_name(name):
    user = find_user_by_name(name)
    if user is None:
        return None
    else:
        return user.id

# finds a User by username
def find_user_by_name(name):
    return User.query.filter_by(username = name).first()

# finds a User by their id
def find_user_by_id(id):
    return User.query.filter_by(id = id).first()

# adds a user to the database
def add_user(name, email, password):
    user = User(name, email, password)
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

# adds a new note to the database corresponding to the current user
def add_new_note(filename, file_contents, username):
    note = Note(filename, file_contents, find_user_id_by_name(username))
    db.session.add(note)
    db.session.commit()
    db.session.refresh(note)

# gets all notes for a specific user
def get_notes_by_user(username):
    user = find_user_by_name(username)
    notes = Note.query.filter_by(user_id = user.id)
    return list(notes)

def find_note_by_name(filename):
    return Note.query.filter_by(filename = filename).first()

# adds a tag to the tag table if it doesn't exist, then links them in the junction table
def add_tag_to_note(filename, tag_name):
    note = find_note_by_name(filename)
    tag = Tag.query.filter_by(tag_name = tag_name).first()
    if tag is None:
        tag = Tag(tag_name)
        db.session.add(tag)
        db.session.commit()
        db.session.refresh(tag)

    note_tag_junction = NoteTagJunction(note.id, tag.id)
    db.session.add(note_tag_junction)
    db.session.commit()
    db.session.refresh(tag)
