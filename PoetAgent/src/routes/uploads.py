from flask import Flask, Blueprint, render_template, request, redirect, url_for
import os

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# Define the blueprint
upload_blueprint = Blueprint('upload', __name__)

# Function to check allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_blueprint.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            # Secure the filename and save the file
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')

@upload_blueprint.route('/uploads/<filename>')
def uploaded_file(filename):
    return f'File uploaded successfully! <br> <img src="/static/images/{filename}" alt="{filename}">'
