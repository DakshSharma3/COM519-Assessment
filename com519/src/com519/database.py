import sqlite3

class Database:
    def __init__(self, db_string):
        self.connection = sqlite3.connect(db_string)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()

    def execute_create_query(self, query):
        # Code to execute a database query
        self.cursor.execute(query)
