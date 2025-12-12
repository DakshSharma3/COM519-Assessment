import sqlite3

from bank_user import User


class Database:
    def __init__(self, db_string):
        self.connection = sqlite3.connect(db_string)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
            
    def disconnect(self):
        """Commits any data and disconnects the database connection   """
        self.connection.commit()
        self.connection.close()

    def create_tables(self):
        """Creates all the tables and necessary entries within the database"""
        table_queries = [
            'CREATE TABLE IF NOT EXISTS Branch ("Branch_ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "Branch_Name" TEXT);',
            'CREATE TABLE IF NOT EXISTS Roles ("Role_ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "Role_Name" TEXT);',
            'CREATE TABLE IF NOT EXISTS Address ("Address_ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "Address" TEXT, "Postcode" TEXT);',
            'CREATE TABLE IF NOT EXISTS People ("People_ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "Forename" TEXT, "Surname" TEXT, "Address_ID" INTEGER REFERENCES Address("Address_ID"), "Phone_Number" INTEGER, "Email" TEXT, "Branch_ID" INTEGER REFERENCES Branch("Branch_ID"));',
            'CREATE TABLE IF NOT EXISTS Employees ("Employee_ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "People_ID" INTEGER REFERENCES People("People_ID"), "Role_ID" INTEGER REFERENCES Roles("Role_ID"), "Employee_Email" TEXT);',
            'CREATE TABLE IF NOT EXISTS Login ("User_ID" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "Username" TEXT, "Password" TEXT, "Encryption_Key" TEXT, "People_ID" INTEGER REFERENCES People("People_ID"), "Employee_ID" INTEGER REFERENCES Employees("Employee_ID"));',
            'CREATE TABLE IF NOT EXISTS Account_Type ( Account_Type_ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, Account_Type TEXT UNIQUE );',
            'CREATE TABLE IF NOT EXISTS Accounts (Account_ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, People_ID INTEGER REFERENCES People (People_ID), Account_Type_ID TEXT REFERENCES Account_type (Account_Type_ID), Balance REAL DEFAULT (0.0));',
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

        account_types = ["Checking", "Saving", "Student", "Joint"]

        for account_type in account_types:
            self.adding_account_type(account_type)

        triggers  = ['CREATE TRIGGER add_employee_id_to_login AFTER INSERT ON Employees FOR EACH ROW BEGIN UPDATE Login SET Employee_ID = NEW.Employee_ID WHERE People_ID = NEW.People_ID; END']

        for trigger in triggers:
            self.execute_create_query(trigger)
            self.connection.commit()

        views = ['CREATE VIEW View_Accounts AS SELECT a.Account_ID, a.People_ID, at.Account_Type, a.balance FROM Accounts a INNER JOIN Account_Type at ON a.Account_Type_ID = at.Account_Type_ID;',
                 'CREATE VIEW People_Info AS SELECT l.User_ID, p.People_ID, p.Forename, p.Surname, a.Address, a.Postcode, p.Phone_number, p.Email, b.Branch_Name, e.Employee_ID, r.Role_Name, e.Employee_Email FROM People p INNER JOIN Login l on p.People_ID = l.People_ID INNER JOIN Address a on a.Address_ID = p.Address_ID INNER JOIN Branch b on b.Branch_ID = p.Branch_ID LEFT JOIN Employees e on p.People_ID = e.People_ID LEFT JOIN Roles r on e.Role_ID = r.Role_ID;']

        for view in views:
            self.execute_create_query(view)
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
        """
        Executes a SQL query

        Args:
            query: query to be executed
        """
        self.cursor.execute(query)

    def format_postcode(self, postcode):
        """
        Formats a postcode

        Args:
            postcode: Postcode to be formatted
        """
        return postcode.upper().replace(" ", "")

    def create_login_entry(self, username, password, encryption_key, people_id):
        """
        Creates a login entry in the database
        Args:
            username: Username inputted by the user in the GUI
            password: Password inputted by the user in the GUI
            encryption_key: Generated encryption key for password
            people_id: ID relating to the already created entry in the People table
        """
        query = """
        INSERT INTO Login (Username, Password, Encryption_Key, People_ID) VALUES (?, ?, ?, ?);
        """
        self.cursor.execute(query, (username, password, encryption_key, people_id))

        self.connection.commit()

    def adding_branch(self, branch_name):
        """
        Adds a branch to the database
        Args:
            branch_name: Branch to be added
        """
        query = """INSERT INTO Branch (Branch_Name) VALUES (?);"""
        self.cursor.execute(query, (branch_name,))
        self.connection.commit()

    def adding_role(self, role_name):
        """
        Adds a role to the database
        Args:
            role_name: Role to be added
        """
        query = """INSERT INTO Roles (Role_Name) VALUES (?);"""
        self.cursor.execute(query, (role_name,))
        self.connection.commit()

    def adding_account_type(self, account_name):
        """
        Adds an Account Type to the database
        Args:
            account_name: Account Type to be added
        """
        query = """INSERT INTO Account_Type (Account_Type) VALUES (?);"""
        self.cursor.execute(query, (account_name,))
        self.connection.commit()

    def username_available(self, username):
        """
        Checks if the username exists in the database
        Args:
            username: Username to be checked

        Returns: true if username is available to use, otherwise false
        """
        query = """SELECT * FROM Login WHERE Username = ?;"""
        results = self.cursor.execute(query, (username,)).fetchall()
        if len(results) <= 0:
            return True
        else:
            return False

    def get_branch_id(self, branch):
        """
        Gets a branch id from the database
        Args:
            branch: Branch to get the ID from

        Returns: branch id
        """
        query = """SELECT Branch_ID FROM Branch WHERE Branch_Name = ?;"""
        results = self.cursor.execute(query, (branch,)).fetchone()
        return results[0]

    def get_account_type_id(self, account_type):
        """
        Gets an account type id from the database
        Args:
            account_type: Account type to get the ID from

        Returns: account type id
        """
        query = """SELECT Account_Type_ID FROM Account_Type WHERE Account_Type = ?;"""
        results = self.cursor.execute(query, (account_type,)).fetchone()
        return results[0]

    def get_user_id(self, username):
        """
        Gets a user id from the database
        Args:
            username: username of the account to get the ID from

        Returns: user id
        """
        query = """SELECT User_ID FROM Login WHERE Username = ?;"""
        results = self.cursor.execute(query, (username,)).fetchone()
        return results[0]
    
    def get_address_id(self, postcode):
        """
        Gets an address id from the database
        Args:
            postcode: Postcode to get the ID from

        Returns: address id
        """
        postcode = self.format_postcode(postcode)
        query = """SELECT Address_ID FROM Address WHERE Postcode = ?;"""
        results = self.cursor.execute(query, (postcode,)).fetchone()
        return results[0]
    
    def address_exists(self, postcode):
        """
        Checks if the address exists in the database
        Args:
            postcode: Postcode to check from

        Returns: true if address exists, otherwise false
        """
        postcode = self.format_postcode(postcode)
        query = """SELECT * FROM Address WHERE Postcode = ?;"""
        results = self.cursor.execute(query, (postcode,)).fetchone()
        if results is None:
            return False
        else:
            return True
        
    def create_address_entry(self, address, postcode):
        """
        Creates an address entry in the database
        Args:
            address: Address to be added
            postcode: Postcode to be added
        """
        postcode = self.format_postcode(postcode)
        query = """INSERT INTO Address (Address, Postcode) VALUES (?, ?);"""
        self.cursor.execute(query, (address, postcode))
        self.connection.commit()

    def get_people_id(self, first_name, surname, phone_number, email, postcode, branch):
        """
        Gets a people id from the database
        Args:
            first_name: First name of the user
            surname:  Surname of the user
            phone_number: Phone number of the user
            email: Email of the user
            postcode: Postcode of the user
            branch: Branch of the user

        Returns: People ID
        """
        branch_id = self.get_branch_id(branch)
        address_id = self.get_address_id(postcode)
        query = """
        SELECT People_ID FROM People 
        WHERE Forename = ? AND Surname = ? AND Address_ID = ? 
        AND Phone_Number = ? AND Email = ? AND Branch_ID = ?;
        """
        results = self.cursor.execute(query, (first_name, surname, address_id, phone_number, email, branch_id)).fetchone()
        return results[0]

    def get_people_id_from_user_id(self,user_id):
        """
        Gets a people id from the database
        :param user_id: the id of the current user logged into the system
        :return: ID of the users general account
        """
        query = """SELECT People_ID FROM Login WHERE User_ID = ?;"""
        results = self.cursor.execute(query, (user_id,)).fetchone()
        return results[0]

    def get_all_user_bank_accounts(self, people_id):
        query = """SELECT * FROM View_Accounts WHERE People_ID = ?;"""
        results = self.cursor.execute(query, (people_id,)).fetchall()
        return results
    
    def get_branch_names(self):
        """Gets all branch names avaliable from the database"""
        query = """SELECT Branch_Name FROM Branch;"""
        results = self.cursor.execute(query).fetchall()
        return results

    def get_account_type_names(self):
        """Gets all account type names avaliable from the database"""
        query = """SELECT Account_Type FROM Account_Type;"""
        results = self.cursor.execute(query).fetchall()
        return results
    
    def register_people(self,first_name, surname, phone_number, email, address, postcode, branch):
        """
        Registers a new person entry in the database
        Args:
            first_name: First name of the user
            surname:  Surname of the user
            phone_number: Phone number of the user
            email: Email of the user
            address: Address of the user
            postcode: Postcode of the user
            branch: Branch of the user

        Returns: True

        """
        if not self.address_exists(postcode):
            self.create_address_entry(address, postcode)
        branch_id = self.get_branch_id(branch)
        address_id = self.get_address_id(postcode)
        query = """INSERT INTO People (Forename, Surname, Address_ID, Phone_Number, Email, Branch_ID) VALUES (?, ?, ?, ?, ?, ?)"""
        self.cursor.execute(query, (first_name, surname, address_id, phone_number, email, branch_id))
        self.connection.commit()
        return True

    def register_account(self, account_type, people_id):
        """
        Creates a new account entry in the database
        :param account_type: The type of bank account to register
        :param people_id: Who owns the account
        :return: True after completion
        """
        query = "INSERT INTO Accounts (Account_Type_ID, People_ID) VALUES (?, ?);"
        self.cursor.execute(query, (account_type, people_id))
        self.connection.commit()
        return True

    def generate_user_object(self, user_id):
        """
        Generates a user object from the database based on what valid login credentials were provided
        :param user_id: The id of the logged in user
        :return: A user object with all relevant data
        """
        query = "SELECT * FROM People_Info WHERE User_ID = ?;"
        result = self.cursor.execute(query, (user_id,)).fetchone()
        user = User(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], (result[9] is not None), result[9], result[10], result[11])
        return user

    def update_bank_balance(self, account_id, new_balance):
        """
        Updates the balance of a users bank account
        :param account_id: id of the account to update
        :param new_balance: new balance to update it to
        """
        query = """UPDATE Accounts SET Balance = ? WHERE Account_ID = ?"""
        self.cursor.execute(query, (new_balance, account_id))
        self.connection.commit()