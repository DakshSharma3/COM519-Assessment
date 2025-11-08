import sqlite3

class Database:
    def __init__(self, db_string):
        self.connection = sqlite3.connect(db_string)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
            
    def disconnect(self):
        self.connection.commit()
        self.connection.close()

    def create_tables(self):
        table_queries = [
            'CREATE TABLE IF NOT EXISTS Branch ("Branch_ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "Branch_Name" TEXT);',
            'CREATE TABLE IF NOT EXISTS Roles ("Role_ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "Role_Name" TEXT);',
            'CREATE TABLE IF NOT EXISTS Address ("Address_ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "Address" TEXT, "Postcode" TEXT);',
            'CREATE TABLE IF NOT EXISTS People ("People_ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "Forename" TEXT, "Surname" TEXT, "Address_ID" INTEGER REFERENCES Address("Address_ID"), "Phone_Number" INTEGER, "Email" TEXT, "Branch_ID" INTEGER REFERENCES Branch("Branch_ID"));',
            'CREATE TABLE IF NOT EXISTS Employees ("Employee_ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "People_ID" INTEGER REFERENCES People("People_ID"), "Role_ID" INTEGER REFERENCES Roles("Role_ID"), "Employee_Email" TEXT);',
            'CREATE TABLE IF NOT EXISTS Login ("User_ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "Username" TEXT, "Password" TEXT, "Encryption_Key" TEXT, "People_ID" INTEGER REFERENCES People("People_ID"), "Employee_ID" INTEGER REFERENCES Employees("Employee_ID"));',
            'CREATE TABLE IF NOT EXISTS Accounts ("Account_ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "People_ID" INTEGER REFERENCES People("People_ID"), "Account_Type" TEXT, "Balance" REAL DEFAULT (0.0));',
            'CREATE TABLE IF NOT EXISTS Appointments ("Appointment_ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "Employee_ID" INTEGER REFERENCES Employees("Employee_ID"), "People_ID" INTEGER REFERENCES People("People_ID"), "Branch_ID" INTEGER REFERENCES Branch("Branch_ID"), "Date" TEXT, "Time" INTEGER, "Purpose" TEXT);'
        ]
    
        for query in table_queries:
            self.execute_create_query(query)

        branches = ["Manchester", "London", "Southampton", "Liverpool", "Cardiff"]

        for branch in branches:
            self.adding_branch(branch)

        roles = ["Financial Advisor", "Loan officer", "Accountant", "Manager"]

        for role in roles:
            self.adding_role(role)

        triggers  = ['CREATE TRIGGER add_employee_id_to_login AFTER INSERT ON Employees FOR EACH ROW BEGIN UPDATE Login SET Employee_ID = NEW.Employee_ID WHERE People_ID = NEW.People_ID; END']

        for trigger in triggers:
            self.execute_create_query(trigger)
            self.connection.commit()

        admin_user_queries = [
            'INSERT INTO Address (Address, Postcode) VALUES ("8 Cranmore","SO315GG");',
            'INSERT INTO People(Forename, Surname, Address_ID, Phone_Number, Email, Branch_ID) VALUES("Daksh", "Sharma", 1, 7401570160, "Daksh@gmail.com", 2);',
            'INSERT INTO Login (Username, Password, Encryption_Key, People_ID) VALUES ("admin", "gAAAAABpDz1yG_0BkQJADCiEtTphDWaEhTzBeDZq8RBqeaQ9Trqac0PGOa0Fy7-ZB3GYjENYYpYn9oE6CD2kDAY34i87su6lDw==", "mD6Zc0wDnggPpdtTQJrBXh9K1RWG6SYJj9SIYSftKkg=", 1);',
            'INSERT INTO Employees (People_ID, Role_ID, Employee_Email) VALUES (1, 4, "Daksh@workEmail.com" );'
        ]
        for query in admin_user_queries:
            self.execute_create_query(query)

        self.connection.commit()



    def execute_create_query(self, query):
        self.cursor.execute(query)

    def format_postcode(self, postcode):
        return postcode.upper().replace(" ", "")

    def create_login_entry(self, username, password, encryption_key, people_id):
        query = """
        INSERT INTO Login (Username, Password, Encryption_Key, People_ID) VALUES (?, ?, ?, ?);
        """
        self.cursor.execute(query, (username, password, encryption_key, people_id))

        self.connection.commit()

    def adding_branch(self, branch_name):
        query = """INSERT INTO Branch (Branch_Name) VALUES (?);"""
        self.cursor.execute(query, (branch_name,))
        self.connection.commit()

    def adding_role(self, role_name):
        query = """INSERT INTO Roles (Role_Name) VALUES (?);"""
        self.cursor.execute(query, (role_name,))
        self.connection.commit()

    def username_available(self, username):
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
        postcode = self.format_postcode(postcode)
        query = """SELECT Address_ID FROM Address WHERE Postcode = ?;"""
        results = self.cursor.execute(query, (postcode,)).fetchone()
        return results[0]
    
    def address_exists(self, postcode):
        postcode = self.format_postcode(postcode)
        query = """SELECT * FROM Address WHERE Postcode = ?;"""
        results = self.cursor.execute(query, (postcode,)).fetchone()
        if results is None:
            return False
        else:
            return True
        
    def create_address_entry(self, address, postcode):
        postcode = self.format_postcode(postcode)
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
        if not self.address_exists(postcode):
            self.create_address_entry(address, postcode)
        branch_id = self.get_branch_id(branch)
        address_id = self.get_address_id(postcode)
        query = """INSERT INTO People (Forename, Surname, Address_ID, Phone_Number, Email, Branch_ID) VALUES (?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(query, (first_name, surname, address_id, phone_number, email, branch_id))
        self.connection.commit()
        return True