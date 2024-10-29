# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 11:22:38 2024

@author: Sajjad Mosharraf
"""
import pandas as pd
import os

def load_data(data_file):
    if not data_file:
        data_file = 'monetization_ded_input_date_mock.csv'
        data_file = os.path.join(os.getcwd(), '..', "data/raw", data_file) 
    data_df = pd.read_csv(data_file, dtype=str, na_values=[' ', 'N\A', '', '\n'])
    return data_df

def clean_data(data_df):
    # Assume data is clean here
    return data_df


def create_graph(data):
    return

# Where to look into to identify root cause
# demand and supply side
def explain_business_relations(keyword):
    business_relation_dict = dict()
    output = business_relation_dict[keyword]
    return

# retun the relation or defnition of business metrics as needed
def explain_business_metrics(keyword):
    business_metrics_dict = dict()
    output = business_relation_dict[keyword]
    return

def identify_key_points(performance_matrix):
    # algorithm for identifying the key points
    # and returning only a portion of the performance_matrix
    return
  

# returns fixed performance_matrix based on provided input
# That is our unque contirbution to calculate performance_matrix
# and indicate the top perfromance metrics for LLM to focus on
def get_performance_matrix(data_file=''):
    # method to get data: now csv, future, db queries
    data_df = load_data(data_file)
    # method to do cleaning
    data_df = clean_data(data_df)
    # method to do math
    # chnage results in a format to be shared with LLM
    return data_df
    

if __name__ == "__main__":
    # test load_data
    print( get_performance_matrix().head())
    
    
