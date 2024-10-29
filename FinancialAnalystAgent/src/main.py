# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 11:25:38 2024

@author: Sajjad Mosharraf
"""
import os
from openai import OpenAI
from UserInput import UserInput
from DataAnalysis import DataAnalysis
from BIAgent import BIAgent
from BAAgent import BAAgent
from SupervisorAgent import SupervisorAgent

def main():
    # Get the details and scope of the work
    seprator = "*" *140
    print(seprator)
    user_input = UserInput()
    api_key = user_input.get_api_key()   
    file_path = user_input.get_file_path()
    analysis_type = user_input.get_analysis_type()
    prompt_type = user_input.get_prompt_type()
    print(seprator)
    # Perform Data Analysis
    data_analysis = DataAnalysis( file_path, analysis_type)
    sale_anomalies  = data_analysis.get_performance_matrix()
    if sale_anomalies.empty:
        sale_anomalies = "There is no anomaly"
    print(sale_anomalies)

    demand_anomalies  = data_analysis.get_demand_matrix()
    if demand_anomalies.empty:
        demand_anomalies = "There is no anomaly"
    print(demand_anomalies)

    supply_anomalies  = data_analysis.get_supply_matrix()
    if supply_anomalies.empty:
        supply_anomalies = "There is no anomaly"
    print(supply_anomalies)

    outlook_anomalies = data_analysis.get_outlook_matrix()
    if outlook_anomalies.empty:
        outlook_anomalies = "There is no anomaly"
    print(outlook_anomalies)
    print(seprator)

    # 1- BI Agent to describe the data
    input_data = {
            "sale_anomalies": sale_anomalies,
            "demand_anomalies": demand_anomalies,
            "supply_anomalies": supply_anomalies
    }
    bi_agent = BIAgent(api_key, prompt_type)
    message = bi_agent.generate_message(input_data)
    print(message)
    
    # 2- BA Agent to demystify the data
    ba_agent = BAAgent(api_key, prompt_type)
    message = ba_agent.generate_message(input_data)
    print(message)

    # 3 - Economist Agent

    # 4- SupervisorAgent
    supervisor_agent = SupervisorAgent(api_key, prompt_type)
    message = supervisor_agent.generate_message(input_data)
    print(message)

if __name__ == "__main__":
    main()