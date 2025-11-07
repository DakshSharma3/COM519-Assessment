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

    def does_username_exist(self, username):
        query = """SELECT * FROM Login WHERE Username = ?;"""
        results = self.cursor.execute(query, (username,)).fetchall()
        if len(results) <= 0:
            return True
        else:
            return False

    def get_branch_id(self, branch):
        query = """SELECT Branch_ID FROM Branch WHERE Branch_Name = ?;"""
        results = self.cursor.execute(query, (branch,)).fetchone()
        return results[0]
    
    def get_address_id(self, postcode):
        postcode = postcode.upper().replace(" ", "")
        query = """SELECT Address_ID FROM Address WHERE Postcode = ?;"""
        results = self.cursor.execute(query, (postcode,)).fetchone()
        return results[0]
    
    def address_exists(self, postcode):
        postcode = postcode.upper().replace(" ", "")
        query = """SELECT * FROM Address WHERE Postcode = ?;"""
        results = self.cursor.execute(query, (postcode,)).fetchone()
        if results is None:
            return False
        else:
            return True
        
    def create_address_entry(self, address, postcode):
        postcode = postcode.upper().replace(" ", "")
        query = """INSERT INTO Address (Address, Postcode) VALUES (?, ?);"""
        self.cursor.execute(query, (address, postcode))
        self.connection.commit()

    def get_people_id(self, first_name, surname, phone_number, email, address, postcode, branch):
        branch_id = self.get_branch_id(branch)
        address_id = self.get_address_id(postcode)
        query = """
        SELECT People_ID FROM People 
        WHERE Forename = ? AND Surname = ? AND Address_ID = ? 
        AND Phone_Number = ? AND Email = ? AND Branch_ID = ?;
        """
        results = self.cursor.execute(query, (first_name, surname, address_id, phone_number, email, branch_id)).fetchone()
        return results[0]
    
    def get_branch_names(self):
        query = """SELECT Branch_Name FROM Branch;"""
        results = self.cursor.execute(query).fetchall()
        return results
    
    def register_people(self,first_name, surname, phone_number, email, address, postcode, branch):
        if self.valid_number(phone_number) and self.valid_email(email):

            if not self.address_exists(postcode):
                self.create_address_entry(address, postcode)
            branch_id = self.get_branch_id(branch)
            address_id = self.get_address_id(postcode)
            query = """INSERT INTO People (Forename, Surname, Address_ID, Phone_Number, Email, Branch_ID) VALUES (?, ?, ?, ?, ?, ?)"""
            self.cursor.execute(query, (first_name, surname, address_id, phone_number, email, branch_id))
            self.connection.commit()
            return True