from flask import Flask, render_template, request
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import random
import openai

app = Flask(__name__)

# Load the BLIP processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image_path):
    """Generate a description for the image."""
    try:
        # Load the image
        image = Image.open(image_path)

        # Preprocess the image and prepare it for the model
        inputs = processor(images=image, return_tensors="pt")

        # Generate the caption
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        
        return caption
    except Exception as e:
        return str(e)

def generate_poem(caption, api_key):
    """Generate a simple poem based on the image."""
    # OpenAI API call to generate a poem based on the caption
    openai.api_key = api_key
    response = openai.Completion.create(
        model="text-davinci-003",  # You can use a different model if needed
        prompt=f"Write a poem about the following caption: {caption}",
        temperature=0.7,
        max_tokens=150
    )
    poem = response.choices[0].text.strip()
    return poem

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    if request.method == 'POST':
        api_key = request.form["api_key"]
        image_path = request.form['image_path']
        option = request.form['option']

        if option == 'Describe the Image':
            result = generate_caption(image_path)
        elif option == 'Poem about the image':
            caption = generate_caption(image_path)
            result = generate_poem(caption)
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
