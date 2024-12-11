import os
import shutil
from flask import Blueprint, render_template, request
from models.generator import InstagramCaptionGenerator
from models.BaseAgent import BaseAgent

# Define the blueprint
main_blueprint = Blueprint('main', __name__)

# Folder where images will be stored
STATIC_IMAGES_FOLDER = 'W:\OMSA\ws\GenerativeAI\PoetAgent\src\static\images'

@main_blueprint.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    image_path = ""
    
    if request.method == 'POST':
        api_key = request.form["api_key"]
        image_path = request.form['image_path']  # Get the image path from the form input
        option = request.form['option']
        theme = request.form['theme']
        persona = request.form['persona']


        # Instantiate the InstagramCaptionGenerator class
        describer = InstagramCaptionGenerator(api_key)
        generator = BaseAgent(api_key, theme, persona)

        # Generate Text description of the image
        img_description = describer.generate_caption(image_path)

        # prepare data to be emded in prompts
        input_data = {
            "caption_theme": theme,
            "image_description": img_description
        }

        # Tailor the output based on user preference
        if option == 'Describe the Image':
            result = img_description
        elif option == 'Poem about the image':
            result = generator.process(input_data)
        elif option == 'Caption for Instagram':
            result = generator.process(input_data) #process

        print(result)

    
    return render_template('index.html', result=result, image_path = image_path)

if __name__ == '__main__':
    image_path = 'static/images/tmp.jpg'
    #'W:\OMSA\ws\GenerativeAI\PoetAgent\src\data\test.jpg'
    image_filename = os.path.basename(image_path)
    destination_path = os.path.join(STATIC_IMAGES_FOLDER, image_filename)
    shutil.copy(image_path, destination_path)