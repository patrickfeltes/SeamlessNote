from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user
import database
import lda

file_routes = Blueprint('file_routes', __name__, template_folder = 'templates')

# main editor page
@file_routes.route('/', methods = ['POST', 'GET'])
@login_required
def home():
    if 'recommended_tags' not in session:
        session['recommended_tags'] = []
    notes = database.get_notes_by_user(current_user.username)
    tag_notes_list = database.get_tag_note_list(current_user.username)
    tag_notes_list.append(('All Notes', database.get_notes_by_user(current_user.username)))

    if request.method == 'GET':
        if 'current_note_name' in session:
            current_note = None
            for note in notes:
                if note.filename == session['current_note_name']:
                    current_note = note
                    break
            if current_note == None:
                return render_template('editor.html', tag_notes_list = tag_notes_list, filename = '', file_contents = '', recommended_tags = session['recommended_tags'])
            else:
                return render_template('editor.html', tag_notes_list = tag_notes_list, filename = current_note.filename, file_contents = current_note.file_contents, recommended_tags = session['recommended_tags'])
        else:
            return render_template('editor.html', tag_notes_list = tag_notes_list, filename = '', file_contents = '', recommended_tags = session['recommended_tags'])

    if 'recommendedTags' in request.form:
        current_note = None
        for note in notes:
            if note.filename == session['current_note_name']:
                current_note = note
                break
        tag = request.form['recommendedTags']
        database.add_tag_to_note(session['current_note_name'], tag, current_user.username)
        return render_template('editor.html', tag_notes_list = tag_notes_list, filename = current_note.filename, file_contents = current_note.file_contents, recommendedTags = session['recommended_tags'])


    # if there are no arguments in the request or the request is to add a file, allow the user to save a new file
    if len(request.form) == 0 or 'addbutton' in request.form:
        session['current_note_name'] = None
        return render_template('editor.html', tag_notes_list = tag_notes_list, filename = '', file_contents = '', recommended_tags = session['recommended_tags'])
    # if there is content in the request and it is a post request, get the file we want and populate the text area with it
    elif request.method == 'POST':
        current_note = None
        for note in notes:
            if note.filename == request.form['button']:
                current_note = note
                break
        session['current_note_name'] = current_note.filename
        # if we can't find the requested note, just populate with empty file contents
        if note is None:
            return render_template('editor.html', tag_notes_list = tag_notes_list, filename = '', file_contents = '', recommended_tags = session['recommended_tags'])
        else:
            return render_template('editor.html', tag_notes_list = tag_notes_list, filename = current_note.filename, file_contents = current_note.file_contents, recommended_tags = session['recommended_tags'])

# saves a file to the database and returns the filename and contents
@file_routes.route('/save', methods = ['GET', 'POST'])
@login_required
def save():
    file_name = ''
    file_contents = ''
    tags = []
    if request.method == 'POST':
        file_name = request.form['filename_field']
        file_contents = request.form['editor']
        # split tags and convert to set of strings
        tags = set(map(lambda x: str(x.strip()), request.form['tags_field'].split(',')))
    else:
        file_name = request.args.get('filename_field')
        file_contents = request.args.get('editor')
        # split tags and convert to set of strings
        tags = set(map(lambda x: str(x.strip()), request.args('tags_field').split(',')))
    
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

    session['recommended_tags'] = lda.suggest_tags(file_contents)

    return redirect(url_for('file_routes.home'))