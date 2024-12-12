"""
Created on Sat Oct  5 10:15:18 2024

@author: Sajjad Mosharraf
"""
from models.BaseAgent import BaseAgent

class BAAgent(BaseAgent):
    """"
    Role:   Business Analyst Agent
    Task:   Analyze the root cause for anomalies in sales, relate it to demand and/or supply
            and generate a root cause analysis report.
            
    Inputs: BI's Reports, 
            Bussiness Relation Information

            It is OK to let LLM use it's economic knowledge.
    """
    def __init__(self, api_key, prompt_type):
        super().__init__(api_key, prompt_type, "ba_prompts.yaml")