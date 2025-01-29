from flask import Flask, render_template, request
from models.employee import Employee
from models.letter_template import LetterTemplate
from models.request_interpretation import RequestInterpreter

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    letter_content = None  # Initialize variable for the letter content
    
    if request.method == 'POST':
        # Get form data from the user
        employee_id = request.form['employee_id']
        reason = request.form['reason']
        due_date = request.form['due_date']
        
        # Create an Employee instance and retrieve the info
        employee = Employee(employee_id)
        employee_info = employee.retrieve_info()
        
        if not employee_info:
            return "Employee not found. Please check the Employee ID."

        # Define the letter_code mapping based on reason
        request_interpreter = RequestInterpreter('generate_letter')
        letter_code = request_interpreter.process(reason)

        if not letter_code:
            return "Invalid reason provided."

        # Generate the letter
        letter_template = LetterTemplate(letter_code, employee_info)
        letter_content = letter_template.generate_letter()
        
    return render_template('index.html', letter=letter_content)
    

if __name__ == '__main__':
    app.run(debug=True)