from openai import OpenAI
import yaml
import os
import json
from dotenv import load_dotenv


prompt_file = 'prompts.yaml'


class RequestInterpreter:
    def __init__(self, request_type):
        """Initialize the RequestInterpreter with the OpenAI API key."""
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        print(self.api_key)
        self.openai_client = OpenAI(api_key = self.api_key)
        self.request_type = request_type


        prompt_file_path = os.path.join(os.getcwd(), "models" , "prompts", prompt_file)
        with open(prompt_file_path, "r") as f:
            self.prompts = yaml.safe_load(f)

        json_file_path = os.path.join(os.getcwd(), "models" , "prompts", request_type + '.json')
        with open(json_file_path) as f:
            self.servavailable_optionsices = json.load(f)

    def generate_message(self, reason):
        system_prompt = self.prompts[self.request_type]["system_prompt"]
        template_user = self.prompts[self.request_type]["template_prompt"]

        input_data = {
            "reason": reason,
            "letter_templates": self.servavailable_optionsices
            }
        user_prompt = template_user.format(**input_data)
        prompt_message = [
            {'role':'system','content':system_prompt},
            {'role':'user','content':user_prompt}
            ]
        return prompt_message

    def generate_response(self, messages, model = "gpt-4o-mini"):
        response = self.openai_client.chat.completions.create(
            model = model,
            messages = messages
            )
        return response.choices[0].message.content
    
    def process(self, reason):
        if self.api_key == "": # Just testing
            letter_code_mapping = {
                "employment verification": 1,
                "cross-border travel": 2,
                "proof of income": 3,
                "proof of work for immigration": 4
            }

            # Identify the letter code based on the reason
            letter_code = letter_code_mapping.get(reason.lower())
            return letter_code

        prompt = self.generate_message(reason)
        return self.generate_response(messages = prompt, model = "gpt-3.5-turbo")
    

if __name__ == "__main__":
    print("TEST")
    request_type = 'generate_letter'
    reason = 'I need to have proof of income for mortage.'
    test_agent = RequestInterpreter(request_type)
    print(test_agent.api_key)
    # prompt_message = test_agent.generate_message(reason)
    # print(prompt_message)