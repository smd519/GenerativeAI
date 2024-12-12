"""
Created on Sat Oct  5 10:15:38 2024

@author: Sajjad Mosharraf
"""
from models.BaseAgent import BaseAgent

class SupervisorAgent(BaseAgent):
    """"
    Role:   Team Lead Agent
    Task:   Review the report from Business Analyst and Economist
            and generate a Bussiness Executive report.
            
    Inputs: Business Analyst's Reports
            Economist Report
    """
    def __init__(self, api_key, prompt_type):
        super().__init__(api_key, prompt_type, "supervisor_prompts.yaml")