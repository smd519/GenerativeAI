"""
Created on Sat Oct  5 10:15:28 2024

@author: Sajjad Mosharraf
"""
from models.BaseAgent import BaseAgent

class BIAgent(BaseAgent):
    """"
    Role:   Business Intelligence Agent
    Task:   Generate a descriptive summary for a given dataset.
            - The summary should be descriptive without any reasoning.
            - The summary should be only based on teh given data and metadata
            - It should not use external source of information e.g. News, Economic knowledge
    """
    def __init__(self, api_key, prompt_type):
        super().__init__(api_key, prompt_type, "bi_prompts.yaml")