"""
to retrieve employee data based on an employee_id
"""
from models.database import Database

class Employee:
    def __init__(self, employee_id):
        """Initialize Employee with employee ID"""
        self.employee_id = employee_id
        self.name = None
        self.job_title = None
        self.income = None
        self.db = Database('employee_database.db')  # assuming SQLite database

    def retrieve_info(self):
        """Retrieve employee information from the database using employee ID"""
        
        """
        TEST TEST

        """
        return {
            "employee_id": self.employee_id,
            "name": 'Martina McBride',
            "job_title": 'Singer',
            "income": '600,000'
        }

        
        # self.db.create_connection()
        
        # query = """
        # SELECT name, job_title, income FROM employees WHERE employee_id = ?
        # """
        # result = self.db.fetch_query(query, (self.employee_id,))
        
        # if result:
        #     self.name, self.job_title, self.income = result[0]  # Assuming single result
        #     self.db.close_connection()
        #     return {
        #         "employee_id": self.employee_id,
        #         "name": self.name,
        #         "job_title": self.job_title,
        #         "income": self.income
        #     }
        # else:
        #     self.db.close_connection()
        #     return None

if __name__ == "__main__":
    print("Test")
    employee_id = 'xyz10'
    employee = Employee(employee_id)
    employee_info = employee.retrieve_info()
    print(employee_info)