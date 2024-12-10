import os
import shutil
from flask import Blueprint, render_template, request
from models.generator import InstagramCaptionGenerator

# Define the blueprint
main_blueprint = Blueprint('main', __name__)

# Folder where images will be stored
STATIC_IMAGES_FOLDER = 'W:\OMSA\ws\GenerativeAI\PoetAgent\src\static\images'

@main_blueprint.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    result_image = ""
    
    if request.method == 'POST':
        api_key = request.form["api_key"]
        image_path = request.form['image_path']  # Get the image path from the form input
        option = request.form['option']
        theme = request.form['theme']
        personality = request.form['personality']

        # Check if the image_path exists
        if os.path.exists(image_path):
            # Generate a new filename (use the basename of the image_path)
            image_filename = os.path.basename(image_path)
            # Create a new path in the static/images folder
            destination_path = os.path.join(STATIC_IMAGES_FOLDER, image_filename)

            # Copy the image to the static/images folder
            shutil.copy(image_path, STATIC_IMAGES_FOLDER)
            result_image = destination_path  # Store relative path for the image

            result_image = os.path.join("static\images", image_filename)

            # Instantiate the InstagramCaptionGenerator class
            generator = InstagramCaptionGenerator(api_key)

            # Generate caption or poem based on user option
            if option == 'Describe the Image':
                result = generator.generate_caption(image_path)
            elif option == 'Poem about the image':
                caption = generator.generate_caption(image_path)
                result = generator.generate_poem(caption)
    
    return render_template('index.html', result=result, result_image=result_image)

if __name__ == '__main__':
    image_path = 'W:\OMSA\ws\GenerativeAI\PoetAgent\src\data\test.jpg'
    image_filename = os.path.basename(image_path)
    destination_path = os.path.join(STATIC_IMAGES_FOLDER, image_filename)
    shutil.copy(image_path, destination_path)