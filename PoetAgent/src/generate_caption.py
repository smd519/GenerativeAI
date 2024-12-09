from transformers import AutoProcessor, AutoModelForImageTextToText
from PIL import Image
import os

def generate_caption(image_path):
    # Load the image
    image = Image.open(image_path)

    # Load the BLIP processor and model from Hugging Face
    processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = AutoModelForImageTextToText.from_pretrained("Salesforce/blip-image-captioning-base")

    # Preprocess the image
    inputs = processor(images=image, return_tensors="pt")

    # Generate the caption
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    
    return caption

if __name__ == "__main__":
    # Test
    image_path = os.path.join(os.getcwd(), "data", "test.jpg")
    caption = generate_caption(image_path)
    print("Generated Caption:", caption)
