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
    filename = db.Column(db.String(100), unique = False)
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
    tag_name = db.Column(db.String(100), unique = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, tag_name, user_id):
        self.tag_name = tag_name
        self.user_id = user_id

    def __repr__(self):
        return 'Tag: ' + self.tag_name + " " + str(self.user_id) 

# NoteTagJunction model for the note_tab_junctions table
class NoteTagJunction(db.Model):
    __tablename__ = 'note_tag_junction'
    id = db.Column(db.Integer, primary_key = True)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, note_id, tag_id, user_id):
        self.note_id = note_id
        self.tag_id = tag_id
        self.user_id = user_id

    def __repr__(self):
        return 'NoteTagJunction: ' + str(self.note_id) + ' ' + str(self.tag_id)

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
# given the old name of a note and the username, update the note
def update_note(old_name, new_name, file_contents, username):
    notes = get_notes_by_user(username)
    note_to_update = None
    for note in notes:
        if note.filename == old_name:
            note_to_update = note
            break
    note_to_update.filename = new_name
    note_to_update.file_contents = file_contents
    db.session.commit()
    db.session.refresh(note_to_update)
# gets all notes for a specific user
def get_notes_by_user(username):
    user = find_user_by_name(username)
    notes = Note.query.filter_by(user_id = user.id)
    return list(notes)

def get_tags_by_user(username):
    return get_tags_by_notes(get_notes_by_user(username))

def get_tags_by_notes(notes):
    tags = []
    for note in notes:
        junctions=list(NoteTagJunction.query.filter_by(note_id = note.id))
        for junction in junctions:
            temp=list(Tag.query.filter_by(id =junction.tag_id))
            if temp is not None and len(temp)!=0:
                tags.extend(temp)
    return tags

def get_notes_by_tag_and_user(username, tag):
    all_notes = get_notes_by_user(username)
    all_tagged_notes = []
    for note in all_notes:
        junctions = NoteTagJunction.query.filter_by(note_id = note.id).all()
        for junction in junctions:
            if tag.id == junction.tag_id:
                all_tagged_notes.append(note)
    return all_tagged_notes

def find_note_by_name(filename):
    return Note.query.filter_by(filename = filename).first()

def get_tag_note_list(username):
    user = find_user_by_name(username)
    tags = Tag.query.filter_by(user_id = user.id).all()
    tag_names = [tag.tag_name.encode('utf-8') for tag in tags]
    tag_names = sorted(tag_names, key = lambda s: s.lower())
    lst = []
    for tag_name in tag_names:
        temp = []
        junctions = NoteTagJunction.query.filter_by(tag_id = tag.id, user_id = user.id).all()
        for junction in junctions:
            temp.append(Note.query.filter_by(id = junction.note_id).first())
        lst.append((tag_name, temp))
    return lst

# adds a tag to the tag table if it doesn't exist, then links them in the junction table
def add_tag_to_note(filename, tag_name, username):
    if len(tag_name.strip()) == 0:
        return
    note = find_note_by_name(filename)
    user = find_user_by_name(username)
    already_existing = Tag.query.filter_by(tag_name = tag_name, user_id = user.id).first()
    print already_existing
    tag = None
    if already_existing == None:
        tag = Tag(tag_name, user.id)
        db.session.add(tag)
        db.session.commit()
        db.session.refresh(tag)
    else:
        tag = already_existing

    note_tag_junction = NoteTagJunction(note.id, tag.id, user.id)
    db.session.add(note_tag_junction)
    db.session.commit()
    db.session.refresh(tag)
