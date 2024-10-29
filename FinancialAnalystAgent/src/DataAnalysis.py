# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 11:25:38 2024
Data Analysis Class:
- load_data
- clean_data
- get_performance_matrix
- get_demand_matrix
- get_supply_matrix
- get_outlook_matrix

@author: Sajjad Mosharraf
"""
import os
import pandas as pd

class DataAnalysis:
    def __init__(self, file_path, analysis_type):
        self.file_path = file_path
        self.analysis_type = analysis_type
        self.data = self.load_data()
        self.clean_data = self.clean_data()
        print(f"Analyzing data from {self.file_path} with {self.analysis_type} approach.")

    def load_data(self):
        print(f"Analyzing data from {self.file_path} with {self.analysis_type} approach.")
        self.file_path = os.path.join(self.file_path)
        data_df = pd.read_csv(self.file_path , dtype=str, na_values=[' ', 'N\A', '', '\n'])
        return data_df

    def clean_data(self):
        clean_data = self.data.copy()
        print("Data Cleaning ... \n\tOriginal shape {}".format(clean_data.shape))

        # Drop rows if  current num AND den are null 
        val_cols = ['current_num', 'current_den']
        clean_data.dropna(subset= val_cols, how='all', inplace=True)

        # Drop row if den = 0
        clean_data = clean_data[clean_data["current_den"] != 0]
        clean_data = clean_data[clean_data["prev_period_den"] != 0]
        clean_data = clean_data[clean_data["prev_year_den"] != 0]
        
        print("\tFinal shape {}".format(clean_data.shape))

        return clean_data

    # returns fixed performance_matrix based on provided input
    def get_performance_matrix(self):
        print("\nCalculating performance matrix ...")
        NetBookings_data = self.clean_data[ 
            (self.clean_data["metric_category_group"] == "Net Bookings (C$)") &
            (self.clean_data["chart_label"].isin(["L7D", "Quarterly-to-date"]))
            ].copy()        

        numeric_cols = [
            "current_num", "current_den", 
            "prev_period_num", "prev_period_den",
            "prev_year_num", "prev_year_den"
            ]
        NetBookings_data[numeric_cols] = NetBookings_data[numeric_cols].apply(pd.to_numeric)
        NetBookings_data["compared_to_previous_perioid_percent"] = NetBookings_data.apply(lambda row: DataAnalysis.prev_period_func(row), axis = 1)
        NetBookings_data["compared_to_previous_year_percent"] = NetBookings_data.apply(lambda row: DataAnalysis.prev_year_fun(row), axis = 1)
        NetBookings_data.drop(numeric_cols , axis=1, inplace= True)
        NetBookings_data.sort_values(by=['product', 'segment', 'region', 'chart_label', 'period_label'], inplace= True)
        NetBookings_data.reset_index(drop=True, inplace=True)
        NetBookings_data = NetBookings_data[
            (NetBookings_data['compared_to_previous_perioid_percent'] > 0) | 
            (NetBookings_data['compared_to_previous_year_percent'] > 0)
            ]
        return NetBookings_data

    def get_demand_matrix(self):
        print("\nCalculating demand matrix ...")
        demand_data = self.clean_data[ 
            (self.clean_data["metric_category_group"].isin(["Budgets", "Budget Utilization"])) &
            (self.clean_data["chart_label"].isin(["L7D", "Quarterly-to-date"]))
            ].copy()
        numeric_cols = [
            "current_num", "current_den", 
            "prev_period_num", "prev_period_den",
            "prev_year_num", "prev_year_den"
            ]
        demand_data[numeric_cols] = demand_data[numeric_cols].apply(pd.to_numeric)
        demand_data["compared_to_previous_perioid_percent"] = demand_data.apply(lambda row: DataAnalysis.prev_period_func(row), axis = 1)
        demand_data["compared_to_previous_year_percent"] = demand_data.apply(lambda row: DataAnalysis.prev_year_fun(row), axis = 1)
        demand_data.drop(numeric_cols , axis=1, inplace= True)
        demand_data.sort_values(by=['product', 'segment', 'region', 'chart_label', 'period_label'], inplace= True)
        demand_data.reset_index(drop=True, inplace=True)
        demand_data = demand_data[
            (demand_data['compared_to_previous_perioid_percent'] > 0) | 
            (demand_data['compared_to_previous_year_percent'] > 0)
            ]

        return demand_data
    
    def get_supply_matrix(self):
        print("\nCalculating supply matrix ...")
        supply_data = self.clean_data[ 
            (self.clean_data["metric_category_group"].isin(["FUV", "EFS", "Inventory", "Matched Requests"])) &
            (self.clean_data["chart_label"].isin(["L7D", "Quarterly-to-date"]))
            ].copy()
        numeric_cols = [
            "current_num", "current_den", 
            "prev_period_num", "prev_period_den",
            "prev_year_num", "prev_year_den"
            ]
        supply_data[numeric_cols] = supply_data[numeric_cols].apply(pd.to_numeric)
        supply_data["compared_to_previous_perioid_percent"] = supply_data.apply(lambda row: DataAnalysis.prev_period_func(row), axis = 1)
        supply_data["compared_to_previous_year_percent"] = supply_data.apply(lambda row: DataAnalysis.prev_year_fun(row), axis = 1)
        supply_data.drop(numeric_cols , axis=1, inplace= True)
        supply_data.sort_values(by=['product', 'segment', 'region', 'chart_label', 'period_label'], inplace= True)
        supply_data.reset_index(drop=True, inplace=True)
        supply_data = supply_data[
            (supply_data['compared_to_previous_perioid_percent'] > 0) | 
            (supply_data['compared_to_previous_year_percent'] > 0)
            ]
        return supply_data
        
    def get_outlook_matrix(self):
        print("\nCalculating outlook matrix ...")
        outlook_data = self.clean_data[ self.clean_data["chart_label"].isin(["Outlook"]) ].copy()
        numeric_cols = [
            "current_num", "current_den", 
            "prev_period_num", "prev_period_den",
            "prev_year_num", "prev_year_den"
            ]
        outlook_data[numeric_cols] = outlook_data[numeric_cols].apply(pd.to_numeric)
        outlook_data["compared_to_previous_perioid_percent"] = outlook_data.apply(lambda row: DataAnalysis.prev_period_func(row), axis = 1)
        outlook_data["compared_to_previous_year_percent"] = outlook_data.apply(lambda row: DataAnalysis.prev_year_fun(row), axis = 1)
        outlook_data.drop(numeric_cols , axis=1, inplace= True)
        outlook_data.sort_values(by=['product', 'segment', 'region', 'chart_label', 'period_label'], inplace= True)
        outlook_data.reset_index(drop=True, inplace=True)
        outlook_data = outlook_data[
            (outlook_data['compared_to_previous_perioid_percent'] > 0) | 
            (outlook_data['compared_to_previous_year_percent'] > 0)
            ]

        return outlook_data

    @staticmethod
    def prev_period_func(row):
        single_cols = ['Budgets', 'Net Bookings (C$)', "FUV", "EFS", "Inventory", "Matched Requests"]
        double_cols = ['Budget Utilization']
        if row['metric_category_group'] in single_cols:
            if row['prev_period_num'] == 0:
                result = 100  # We just show good progress for new product
            else:
                a = row['current_num']
                b = row['prev_period_num']
                result = (a-b)/b*100
        
        elif row['metric_category_group'] in double_cols:
            if row['prev_period_num'] == 0:
                result = 100 
            else:
                a = row['current_num'] / row['current_den'] 
                b = row['prev_period_num'] / row['prev_period_den'] 
                result = (a-b)/b*100

        return round(result, 2)

    @staticmethod
    def prev_year_fun(row):
        single_cols = ['Budgets', 'Net Bookings (C$)', "FUV", "EFS", "Inventory", "Matched Requests"]
        double_cols = ['Budget Utilization']
        if row['metric_category_group'] in single_cols:
            if row['prev_year_num'] == 0:
                result = 100 
            else:
                a = row['current_num']
                b = row['prev_year_num']
                result = (a-b)/b*100
        
        elif row['metric_category_group'] in double_cols:
            if row['prev_year_num'] == 0:
                result = 100 
            else:
                a = row['current_num'] / row['current_den'] 
                b = row['prev_year_num'] / row['prev_year_den'] 
                result = (a-b)/b*100

        return round(result, 2)

    
if __name__ == "__main__":
    # test
    file_path = os.path.join(os.getcwd(), "data", "raw", "monetization_ded_input_date_mock.csv")
    data_analysis = DataAnalysis(file_path, "Overall Analysis")
    data_analysis.get_performance_matrix()
    data_analysis.get_demand_matrix()
    data_analysis.get_supply_matrix()
    data_analysis.get_outlook_matrix()
