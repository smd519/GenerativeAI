This project is a web application designed to help social media influencers and content creators effortlessly generate captivating captions for their posts.
+ The app processes the uploaded image *locally* using a pretrained [BLIP model](https://github.com/salesforce/BLIP) to generate a textual description of the image.
+ Then it dynamically creates a detailed prompts using textual description of the image, and user-defined preferences such as tone (formal, casual, fun) and persona (fashion, travel, tech blogger, etc.).
+ Once the prompt is generated, it is sent to OpenAI’s API to craft a relevant caption for social media posts.

<img src=screenshots/Options.jpg alt="Alt Text" width="200"> <img src=screenshots/Theme.jpg alt="Alt Text" width="200">

<img src=screenshots/Output.jpg alt="Alt Text" width="600">




