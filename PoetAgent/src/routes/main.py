from flask import Blueprint, render_template, request
from models.generator import InstagramCaptionGenerator

# Definiton of the blueprints
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    if request.method == 'POST':
        api_key = request.form["api_key"]
        image_path = request.form['image_path']
        option = request.form['option']

        # Instantiate the InstagramCaptionGenerator class
        generator = InstagramCaptionGenerator(api_key)

        if option == 'Describe the Image':
            result = generator.generate_caption(image_path)
        elif option == 'Poem about the image':
            caption = generator.generate_caption(image_path)
            result = generator.generate_poem(caption)
    
    return render_template('index.html', result=result)
