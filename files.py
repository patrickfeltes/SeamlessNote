from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import database

file_routes = Blueprint('file_routes', __name__, template_folder = 'templates')

# main editor page
@file_routes.route('/', methods = ['POST', 'GET'])
@login_required
def home():
    notes = database.get_notes_by_user(current_user.username)
    # on first request of the page, there is nothing in the post request
    if len(request.form) == 0:
        return render_template('editor.html', notes = notes, file_contents = '')
    # if there is content in the request and it is a post request, get the file we want and populate the text area with it
    elif request.method == 'POST':
        current_note = None
        for note in notes:
            if note.filename == request.form['button']:
                current_note = note
                break
        # if we can't find the requested note, just populate with empty file contents
        if note is None:
            return render_template('editor.html', notes = notes, file_contents = '')
        else:
            return render_template('editor.html', notes = notes, file_contents = current_note.file_contents)


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
    database.add_new_note(file_name, file_contents, current_user.username)
    # all all of the tags to the note
    for tag in tags:
        database.add_tag_to_note(file_name, tag)
    return file_name + file_contents