# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 11:25:38 2024

@author: Sajjad Mosharraf
"""
import json
import os

class UserInput:
    def __init__(self):
        self.file_path = ""
        self.api_key = ""
        self.analysis_type = ""
        self.prompt_type = ""

    def get_file_path(self):
        self.file_path = input("Enter the path to the file: ")
        self.save_file_path()
        return self.file_path

    def get_api_key(self):
        self.api_key = input("Enter your API key: ")
        return self.api_key

    def get_prompt_type(self):
        self.prompt_type = input("Enter prompt type (e.g., zero_shot, one_shot, few_shot, react, react_cot): ")
        return self.prompt_type

    def get_analysis_type(self):
        print("Select analysis type:")
        print("1. Overall Analysis")
        print("2. Detailed Analysis")
        choice = input("Enter your choice (1 or 2): ")
        if choice == "1":
            self.analysis_type = "Overall Analysis"
            print(f"You selected: {self.analysis_type}")

        elif choice == "2":
            self.analysis_type = "Detailed Analysis"
            Product = input("Enter your Product: ")
            Segment = input("Enter your Segment: ")
            Region = input("Enter your Region: ")
            print(f"You selected: {self.analysis_type} for {Product}, {Segment}, {Region}")
        
        return self.analysis_type

    def save_file_path(self):
        directory = os.path.join(os.getcwd(), "usr")
        if not os.path.exists(directory):
            os.makedirs(directory)
        user_input_file = os.path.join(directory, "user_input.json")
        data = {
            "file_path": self.file_path
        }
        with open(user_input_file, "w") as f:
            json.dump(data, f, indent=4)
        return user_input_file

if __name__ == "__main__":
    user_input = UserInput()
    user_input.get_api_key()
    user_input.get_file_path()
    user_input.get_analysis_type()
    user_input.get_prompt_type()