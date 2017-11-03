import models

# given a user name, find the unique id associated with that user
# if that user doesn't exist, return None
def find_user_id_by_name(db, name):
    user = find_user_by_name(db, name)
    if user is None:
        return None
    else:
        return user.id

# finds a User by username
def find_user_by_name(db, name):
    return models.User.query.filter_by(username = name).first()

# finds a User by their id
def find_user_by_id(db, id):
    return models.User.query.filter_by(id = id).first()

# adds a user to the database
def add_user(db, name, email, password):
    user = models.User(name, email, password)
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

# adds a new note to the database corresponding to the current user
def add_new_note(db, filename, file_contents, username):
    note = models.Note(filename, file_contents, find_user_id_by_name(db, username))
    db.session.add(note)
    db.session.commit()
    db.session.refresh(note)