class User:
    def __init__(self, people_id, forename, surname, address, postcode, phone_number, email, branch, is_employee, employee_id = None, role = None, employee_email = None):
        self.__people_id = people_id
        self.__forename = forename
        self.__surname = surname
        self.__address = address
        self.__postcode = postcode
        self.__phone_number = phone_number
        self.__email = email
        self.__branch  = branch
        self.__is_employee = is_employee
        self.__employee_id = employee_id
        self.__role = role
        self.__employee_email = employee_email
        self.__appointments = []
        self.__accounts = []
        # Import added here to avoid circular import error
        from com519.database import Database
        self.database_name = "COM519.db"
        self.db = Database(self.database_name)

    def get_people_id(self):
        return self.__people_id

    def get_forename(self):
        return self.__forename

    def set_forename(self, forename):
        self.__forename = forename

    def get_surname(self):
        return self.__surname

    def set_surname(self, surname):
        self.__surname = surname

    def get_address(self):
        return self.__address

    def set_address(self, address):
        self.__address = address

    def get_postcode(self):
        return self.__postcode

    def set_postcode(self, postcode):
        self.__postcode = postcode

    def get_phone_number(self):
        return self.__phone_number

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_branch(self):
        return self.__branch

    def set_branch(self, branch):
        self.__branch = branch

    def get_is_employee(self):
        return self.__is_employee

    def set_is_employee(self, is_employee):
        self.__is_employee = is_employee

    def get_employee_id(self):
        return self.__employee_id

    def get_role(self):
        return self.__role

    def set_role(self, role):
        self.__role = role

    def get_employee_email(self):
        return self.__employee_email

    def set_employee_email(self, employee_email):
        self.__employee_email = employee_email

    def get_appointments(self):
        return self.__appointments

    def load_appointments(self):
        query = """SELECT Appointment_ID FROM Appointments WHERE People_ID = ?;"""
        query = """SELECT Appointment_ID FROM Appointments WHERE Employee_ID = ?;"""






