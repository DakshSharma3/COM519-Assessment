import tkinter as tk
from functools import partial
from tkinter import ttk, messagebox

from cryptography.fernet import Fernet

from database import Database


class Register(tk.Toplevel):
    def __init__(self, parent, username_entry, password_entry):
        super().__init__(parent)
        self.database_name = "C:\\Users\\e465565\\Desktop\\Git Repos\\COM519\\COM519-Assessment\\com519\\src\\com519\\COM519.db"
        self.title("My Tkinter App")
        self.geometry("400x500")
        self.username = username_entry.get()
        self.password = password_entry.get()
        forename = tk.StringVar()
        surname = tk.StringVar()
        address = tk.StringVar()
        postcode = tk.StringVar()
        phone_number = tk.StringVar()
        email = tk.StringVar()
        branch = tk.StringVar()
        self.db = Database(self.database_name)



        username_text = tk.Label(self, text="Username: ", font=("Arial", 16))
        username_text.grid(column=0, row=0, padx=10, pady=10)

        username_entry = tk.Entry(self, textvariable=self.username)
        username_entry.grid(column=1, row=0, padx=10, pady=10)
        username_entry.delete(0, tk.END)
        username_entry.insert(0, self.username)

        password_text = tk.Label(self, text="Password: ", font=("Arial", 16))
        password_text.grid(column=0, row=1, padx=10, pady=10)

        password_entry = tk.Entry(self, textvariable=self.password, show="*")
        password_entry.grid(column=1, row=1, padx=10, pady=10)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, self.password)

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

        branch_dropdown = ttk.Combobox(self, values=self.db.get_branch_names(), textvariable=branch, state="readonly")
        branch_dropdown.grid(column=1, row=8, padx=10, pady=10)

        register_button = tk.Button(self, text="Register", command=partial(self.register, username_entry, password_entry, forename_entry, surname_entry, phone_number_entry, email_entry, address_entry, postcode_entry, branch) )
        register_button.grid(column=1, row=9, padx=10, pady=10)

    def display(self, username, password, first_name, surname, phone_number, email, address, postcode, branch):
        print(username.get())
        print(password.get())
        print(first_name.get())
        print(surname.get())
        print(phone_number.get())
        print(email.get())
        print(address.get())
        print(postcode.get())
        print(branch.get())

    def valid_password(self, password):
        valid_length = len(password) >= 8
        has_digit = any(character.isdigit() for character in password)
        has_uppercase = any(character.isupper() for character in password)
        has_symbol = any(not character.isalnum() for character in password)

        if valid_length and has_digit and has_uppercase and has_symbol:
            return True
        else:
            return False

    def valid_number(self, number):
        valid_digit = number.get().isdigit() and len(number.get()) == 11
        return valid_digit

    def valid_email(self, email):
        valid_email = any(character == "@" for character in email.get())
        return valid_email

    def register(self, username, password, first_name, surname, phone_number, email, address, postcode, branch):
        username = username.get()
        password = password.get()
        if self.db.username_available(username):
            if self.valid_password(password):
                key = Fernet.generate_key()
                cipher = Fernet(key)
                password = cipher.encrypt(password.encode())
                if self.valid_number(phone_number) and self.valid_email(email):
                    self.db.register_people(first_name.get(), surname.get(), phone_number.get(), email.get(), address.get(), postcode.get(), branch.get())
                people_id = self.db.get_people_id(first_name.get(), surname.get(), phone_number.get(), email.get(), address.get(), postcode.get(), branch.get())
                self.db.create_login_entry(username, password, key, people_id)
                messagebox.showinfo("Information", "Registration Successful")
                self.db.disconnect()
            else:
                messagebox.showerror("Error", "Registration Failed, password does not meet requirements\n\n- 8 or more characters\n- Contains a capital letter\n- Contains a number\n- Contains a special character")
                self.db.disconnect()
        else:
            messagebox.showerror("Error", "Registration Failed, username may already exist")
            self.db.disconnect()


