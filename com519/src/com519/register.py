import tkinter as tk
from functools import partial
from operator import truediv
from tkinter import ttk, messagebox

from cryptography.fernet import Fernet

from database import Database


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Tkinter App")
        self.geometry("400x500")
        username = tk.StringVar()
        password = tk.StringVar()
        forename = tk.StringVar()
        surname = tk.StringVar()
        address = tk.StringVar()
        postcode = tk.StringVar()
        phone_number = tk.StringVar()
        email = tk.StringVar()
        branch = tk.StringVar()



        username_text = tk.Label(self, text="Username: ", font=("Arial", 16))
        username_text.grid(column=0, row=0, padx=10, pady=10)

        username_entry = tk.Entry(self, textvariable=username)
        username_entry.grid(column=1, row=0, padx=10, pady=10)

        password_text = tk.Label(self, text="Password: ", font=("Arial", 16))
        password_text.grid(column=0, row=1, padx=10, pady=10)

        password_entry = tk.Entry(self, textvariable=password, show="*")
        password_entry.grid(column=1, row=1, padx=10, pady=10)

        forename_text = tk.Label(self, text="First Name: ", font=("Arial", 16))
        forename_text.grid(column=0, row=2, padx=10, pady=10)

        forename_entry = tk.Entry(self, textvariable=forename)
        forename_entry.grid(column=1, row=2, padx=10, pady=10)

        surname_text = tk.Label(self, text="Last Name: ", font=("Arial", 16))
        surname_text.grid(column=0, row=3, padx=10, pady=10)

        surname_entry = tk.Entry(self, textvariable=surname)
        surname_entry.grid(column=1, row=3, padx=10, pady=10)

        address_text = tk.Label(self, text="Address: ", font=("Arial", 16))
        address_text.grid(column=0, row=4, padx=10, pady=10)

        address_entry = tk.Entry(self, textvariable=address)
        address_entry.grid(column=1, row=4, padx=10, pady=10)

        postcode_text = tk.Label(self, text="Postcode: ", font=("Arial", 16))
        postcode_text.grid(column=0, row=5, padx=10, pady=10)

        postcode_entry = tk.Entry(self, textvariable=postcode)
        postcode_entry.grid(column=1, row=5, padx=10, pady=10)

        phone_number_text = tk.Label(self, text="Phone number: ", font=("Arial", 16))
        phone_number_text.grid(column=0, row=6, padx=10, pady=10)

        phone_number_entry = tk.Entry(self, textvariable=phone_number)
        phone_number_entry.grid(column=1, row=6, padx=10, pady=10)

        email_text = tk.Label(self, text="Email: ", font=("Arial", 16))
        email_text.grid(column=0, row=7, padx=10, pady=10)

        email_entry = tk.Entry(self, textvariable=email)
        email_entry.grid(column=1, row=7, padx=10, pady=10)

        branches = ["Southampton", "Oxford", "London", "Liverpool"]

        branch_text = tk.Label(self, text="Branch: ", font=("Arial", 16))
        branch_text.grid(column=0, row=8, padx=10, pady=10)

        branch_dropdown = ttk.Combobox(self, values=branches, textvariable=branch, state="readonly")
        branch_dropdown.grid(column=1, row=8, padx=10, pady=10)

        register_button = tk.Button(self, text="Register", command=partial(self.valid_email, email_entry) )
        register_button.grid(column=1, row=9, padx=10, pady=10)  # partial(self.register, username_entry, password_entry)


    def valid_username(self, username, db):
        query = """SELECT * FROM Login WHERE Username = ?;"""
        results = db.cursor.execute(query, (username,)).fetchall()
        print(len(results))
        if len(results) <= 0:
            return True
        else:
            return False

    def valid_password(self, password, db):
        valid_length = len(password) >= 8
        has_digit = any(character.isdigit() for character in password)
        has_uppercase = any(character.isupper() for character in password)
        has_symbol = any(character.isalnum() for character in password)

        if valid_length and has_digit and has_uppercase and has_symbol:
            return True
        else:
            return False

    def register_people(self,phone_number, email, address, postcode, branch):
        if self.valid_number(phone_number) and self.valid_email(email):
            db = Database("login.db")
            if not self.address_exists():
                self.create_address_entry(address, postcode, db)
                branch_id = self.get_branch_id(branch, db)

    def get_branch_id(self, branch, db):
        query = """SELECT Branch ID FROM Branch WHERE Branch = ?;"""
        results = db.cursor.execute(query, (branch,)).fetchone()
        return results[0]

    def get_address_id(self, postcode, db):
        postcode = postcode.get().trim().upper()
        query = """SELECT Address ID FROM Address WHERE Postcode = ?;"""
        results = db.cursor.execute(query, (postcode,)).fetchone()
        return results[0]

    def address_exists(self, postcode, db):
        postcode = postcode.get().trim().upper()
        query = """SELECT * FROM Address WHERE Postcode = ?;"""
        results = db.cursor.execute(query, (postcode,)).fetchall()
        if len(results) > 0:
            return True
        else:
            return False

    def create_address_entry(self, address, postcode, db):
        query = """INSERT INTO Address (Address, Postcode) VALUES (?, ?);"""
        db.cursor.execute(query, (address.get(), postcode.get()))
        db.connection.commit()

    def valid_number(self, number):
        valid_digit = number.get().isdigit() and len(number.get()) == 11
        return valid_digit

    def valid_email(self, email):
        valid_email = any(character == "@" for character in email.get())
        return valid_email

    def register(self, username, password):
        username = username.get()
        password = password.get()
        db = Database("login.db")
        if self.valid_username(username, db):
            if self.valid_password(password, db):
                key = Fernet.generate_key()
                cipher = Fernet(key)
                password = cipher.encrypt(password.encode())
                query = """
                INSERT INTO Login (Username, Password, key) VALUES (?, ?, ?);
                """
                db.cursor.execute(query, (username, password, key))
                db.connection.commit()
                messagebox.showinfo("Information", "Registration Successful")
                db.disconnect()
            else:
                messagebox.showerror("Error", "Registration Failed, password does not meet requirements\n\n- 8 or more characters\n- Contains a capital letter\n- Contains a number\n- Contains a special character")
                db.disconnect()
        else:
            messagebox.showerror("Error", "Registration Failed, username may already exist")
            db.disconnect()


main = Main()
main.mainloop()