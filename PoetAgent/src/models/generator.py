import openai
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import warnings

# Disable warnings about importing the trained models
#warnings.filterwarnings("ignore")

# Load the BLIP processor and model for captioning
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

class InstagramCaptionGenerator:
    def __init__(self, api_key=None):

        if api_key:
            openai.api_key = api_key

    def generate_caption(self, image_path):
        """ Image to to Text """
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

    def generate_poem(self, caption):
        """Generate a simple poem based on the caption."""
        try:
            # OpenAI API call to generate a poem based on the caption
            response = openai.Completion.create(
                model="text-davinci-003",  # You can use a different model if needed
                prompt=f"Write a poem about the following caption: {caption}",
                temperature=0.7,
                max_tokens=150
            )
            poem = response.choices[0].text.strip()
            return poem
        except Exception as e:
            return str(e)

# if __name__ == '__main__':
#     test_key = "ssssss"
#     icg = InstagramCaptionGenerator(test_key)