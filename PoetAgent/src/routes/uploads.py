from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Define the blueprint
upload_blueprint = Blueprint('uploads', __name__)

# Function to clean up the images folder

def clean_images_folder():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)  # Delete the file

# Function to check allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_blueprint.route('/upload', methods=['POST'])
def upload_image():
    file = request.files.get('image_file')
    print("******************************")
    clean_images_folder()
    if file and allowed_file(file.filename):
        # Secure the filename and save the file
        filename , file_extension = os.path.splitext(secure_filename(file.filename))
        filename = 'tmp' + file_extension
        #filename = secure_filename(file.filename)
        try:
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        except:
            print("Failed to upload the image.")
        else:
            print("Image uploaded successfully.")

        #return redirect(url_for('uploads.uploaded_file', filename=filename))
        return jsonify({'image_path': f'static/images/{filename}'})

    #return 'Invalid file type or no file uploaded', 400
    return jsonify({'error': 'Invalid file type'})

@upload_blueprint.route('/uploads/<filename>')
def uploaded_file(filename):
    """Display the uploaded image."""
    return f'File uploaded successfully! <br> <img src="/static/images/{filename}" alt="{filename}">'
