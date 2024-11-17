# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 11:25:38 2024

@author: Sajjad Mosharraf
"""
# from actions import get_response_time
# from prompts import system_prompt

import os
import yaml
from openai import OpenAI
import pandas as pd 

class BaseAgent:
    """"
    Role:   Base Agent
    Task:   To Select the right Prompt form the list
            and create a communication channel between LLM and user.
    """
    def __init__(self, api_key, prompt_type, prompt_file):
        self.api_key = api_key
        self.prompt_type = prompt_type
        self.openai_client = OpenAI(api_key = self.api_key)

        file_path = os.path.join(os.getcwd(), "prompts", prompt_file)
        with open(file_path, "r") as f:
            self.prompts = yaml.safe_load(f)

    def generate_message(self, input_data):
        template_content = self.prompts[self.prompt_type]["template_prompt"]
        system_prompt = self.prompts[self.prompt_type]["system_prompt"]
        # Convert DataFrames to markdown tables
        #formatted_data = {k: v.to_markdown() for k, v in input_data.items()}
        content = template_content.format(**input_data )
        template_message = [
            {'role':'system','content':system_prompt},
            {'role':'user','content':content}
            ]
        return template_message
    
    def generate_response(self, messages, model = "gpt-4o-mini"):  
        # OpenAI documents recommend choosing gpt-4o-mini where you would have previously used gpt-3.5-turbo
        response = self.openai_client.chat.completions.create(
            model = model,
            messages = messages
            )
        return response.choices[0].message.content

    def process(self, input_data):
        prompt = self.generate_message(input_data)
        return self.generate_response(messages = prompt, model = "gpt-3.5-turbo")
    
if __name__ == "__main__":
    test_agent = BaseAgent(api_key= "jhggdhdhsd", prompt_type= "cot", prompt_file= 'bi_prompts.yaml')
    print("************\n")
    print(test_agent.prompts[test_agent.prompt_type]["template-prompt"])
    print("************\n")
    d = {'col1': [1, 2, "Here I am"], 'col2': [3, 4, "Because I am"]}
    df1 = pd.DataFrame(data=d)
    df2 = df1.copy()
    df3 = df1.copy()
    input_data = {
            "sale_anomalies": df1,
            "demand_anomalies": df2,
            "supply_anomalies": df3
    }
    message = test_agent.generate_message(input_data)
    print(message)
