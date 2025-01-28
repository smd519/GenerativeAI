import json
from os import path

class LetterTemplate:
    def __init__(self, letter_code, employee_info):
        self.letter_code = letter_code # Later chnage this to just file name
        self.employee_info = employee_info 
        self.template_file = self.get_template_file()

    def get_template_file(self):
        # Load the mapping from request_type.json
        try:
            with open('models/request_type.json') as f:
                request_type_mapping = json.load(f)
            
            # Get the template filename based on the letter_code
            template_filename = request_type_mapping.get(str(self.letter_code))
            if not template_filename:
                raise ValueError(f"No template found for letter code: {self.letter_code}")
            return template_filename
        
        except Exception as e:
            print(f"Error loading template file: {e}")
            return None
        

    def generate_letter(self):
        """
        Generate the letter content by filling in the template with employee info.
        """
        if not self.template_file:
            return "Template file not found."
        
        # Load the template from file
        try:
            template_path = path.join("models", "samples_letters", self.template_file)
            with open(template_path, 'r') as template_file:
                template_content = template_file.read()
            
            # Replace placeholders in the template with actual employee info
            # Replace later with a more generic approach
            letter_content = template_content.format(
                name=self.employee_info["name"],
                employee_id=self.employee_info["employee_id"],
                job_title=self.employee_info["job_title"],
                income=self.employee_info["income"]
            )

            return letter_content

        except Exception as e:
            print(f"Error loading or processing the template: {e}")
            return "Error generating the letter."
