# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 11:25:38 2024

@author: sdm519
"""
# from actions import get_response_time
# from prompts import system_prompt

import os
import yaml
from openai import OpenAI
import pandas as pd 

prompt_file = 'prompts.yaml'

class BaseAgent:
    """"
    Role:   Base Agent
    Task:   To Select the right Prompt form the list
            and create a communication channel between LLM and user.
    """
    def __init__(self, api_key, theme, persona):
        self.api_key = api_key
        self.theme = theme
        self.persona = persona
        self.openai_client = OpenAI(api_key = self.api_key)

        file_path = os.path.join(os.getcwd(), "src", "models" , "prompts", prompt_file)
        with open(file_path, "r") as f:
            self.prompts = yaml.safe_load(f)

    def generate_message(self, input_data):
        template_content = self.prompts[self.persona]["template_prompt"]
        system_prompt = self.prompts[self.persona]["system_prompt"]
        content = template_content.format(**input_data )
        template_message = [
            {'role':'system','content':system_prompt},
            {'role':'user','content':content}
            ]
        return template_message
    
    def generate_response(self, messages, model = "gpt-4o-mini"):
        response = self.openai_client.chat.completions.create(
            model = model,
            messages = messages
            )
        return response.choices[0].message.content

    def process(self, input_data):
        prompt = self.generate_message(input_data)
        return self.generate_response(messages = prompt, model = "gpt-3.5-turbo")
    
if __name__ == "__main__":
    test_agent = BaseAgent(api_key= "jhggdhdhsd", theme = 'Fun', persona = 'Travel Blogger')
    print("************\n")
    print(test_agent.prompts[test_agent.persona]["template_prompt"])
    print("************\n")
    d = {'col1': [1, 2, "Here I am"], 'col2': [3, 4, "Because I am"]}
    df1 = pd.DataFrame(data=d)
    df2 = df1.copy()
    df3 = df1.copy()
    input_data = {
            "caption_theme": df1,
            "image_description": df2
    }
    message = test_agent.generate_message(input_data)
    print(message)
