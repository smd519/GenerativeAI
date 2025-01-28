"""
handles database connection
"""
import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_file):
        """Initialize the Database connection"""
        self.db_file = db_file
        self.conn = None

    def create_connection(self):
        """Create a connection to the SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            print("Connection to SQLite DB successful.")
        except Error as e:
            print(f"Error while connecting to database: {e}")
            self.conn = None

    def close_connection(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=()):
        """Execute a single query"""
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor
        else:
            print("No database connection established.")
            return None

    def fetch_query(self, query, params=()):
        """Fetch results for a query"""
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return rows
        else:
            print("No database connection established.")
            return None

if __name__ == "__main__":
    print("Hello, World!")