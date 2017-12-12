from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user
import database
import lda

file_routes = Blueprint('file_routes', __name__, template_folder = 'templates')

# There are 3 number of types of editor pages
# 1. A blank page occurs when a user presses the add button or loads the page after logging in.
# 2. A page with file contents and recommended tags. Is a GET request which only occurs after a user saves a note.
# 3. A page with file contents and no recommended tags. This occurs when the user selects a note from the sidebar.
@file_routes.route('/', methods = ['POST', 'GET'])
@login_required
def home():
    if 'recommended_tags' not in session:
        session['recommended_tags'] = []
    (tag_notes_list, notes) = get_sidebar_info()

    # request is a get when a file is saved
    if request.method == 'GET':
        if 'current_note_name' not in session:
            return render_blank(tag_notes_list)
        
        current_note = find_note(notes, session['current_note_name'])
        return render_editor(tag_notes_list, current_note.filename, current_note.file_contents, session['recommended_tags'])
    else:
        # the only time we want recommended tags in when a user saves a file, which is only a get request
        session['recommended_tags'] = []

        if 'recommendedTags' in request.form:
            current_note  = find_note(notes, session['current_note_name'])
            tag = request.form['recommendedTags']
            database.add_tag_to_note(session['current_note_name'], tag, current_user.username)
            return render_editor(tag_notes_list, current_note.filename, current_note.file_contents, [])

        # if there are no arguments in the request or the request is to add a file, allow the user to save a new file
        if len(request.form) == 0 or 'addbutton' in request.form:
            session['current_note_name'] = None
            return render_blank(tag_notes_list)
        # if there is content in the request and it is a post request, get the file we want and populate the text area with it
        else:
            note = find_note(notes, request.form['button'])
            session['current_note_name'] = note.filename
            # if we can't find the requested note, just populate with empty file contents
            if note is None:
                return render_blank(tag_notes_list)
            else:
                return render_editor(tag_notes_list, note.filename, note.file_contents, [])

# helper method to find a note by filename
def find_note(notes, filename):
    for note in notes:
        if note.filename == filename:
            return note
    return None

# helper method to render the editor
def render_editor(tag_notes_list, filename, file_contents, recommended_tags):
    return render_template('editor.html', tag_notes_list = tag_notes_list, filename = filename, file_contents = file_contents, recommended_tags = recommended_tags)

# renders a blank editor page
def render_blank(tag_notes_list):
    return render_editor(tag_notes_list, '', '', [])

def get_sidebar_info():
    notes = database.get_notes_by_user(current_user.username)
    tag_notes_list = database.get_tag_note_list(current_user.username)
    tag_notes_list.append(('All Notes', database.get_notes_by_user(current_user.username)))
    return (tag_notes_list, notes)

# saves a file to the database and returns the filename and contents
@file_routes.route('/save', methods = ['GET', 'POST'])
@login_required
def save():
    file_name = request.form['filename_field']
    file_contents = request.form['editor']
    # split tags and convert to set of strings
    tags = set(map(lambda x: str(x.strip()), request.form['tags_field'].split(',')))
    
    # if there is a current file, we need to update it, not try to make a new entry
    if 'current_note_name' in session and session['current_note_name'] is not None:
        database.update_note(session['current_note_name'], file_name, file_contents, current_user.username)
        session['current_note_name'] = file_name
    else:
        database.add_new_note(file_name, file_contents, current_user.username)
        session['current_note_name'] = file_name
        
    # add tags to notes
    for tag in tags:
        database.add_tag_to_note(file_name, tag, current_user.username)

    # run lda code to suggest 
    session['recommended_tags'] = lda.suggest_tags(file_contents)

    return redirect(url_for('file_routes.home'))