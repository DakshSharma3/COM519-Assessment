# tkinter_app/main.py

import tkinter as tk
from tkinter import messagebox
from functools import partial
from tkinter import ttk
from cryptography.fernet import Fernet

from database import Database
import os

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        # self.create_database()
        self.title("My Tkinter App")
        self.geometry("400x150")
        username = tk.StringVar()
        password = tk.StringVar()        

        username_text = tk.Label(self, text="Username: ", font=("Arial", 16))
        username_text.grid(column=0, row=0, padx=10, pady=10)

        username_entry = tk.Entry(self, textvariable=username)
        username_entry.grid(column=1, row=0, padx=10, pady=10)


        password_text = tk.Label(self, text="Password: ", font=("Arial", 16))
        password_text.grid(column=0, row=1, padx=10, pady=10)


        password_entry = tk.Entry(self, textvariable=password, show="*")
        password_entry.grid(column=1, row=1, padx=10, pady=10)

        login_button = tk.Button(self, text="Login", command= partial(self.login, username_entry, password_entry))
        login_button.grid(column=0, row=2, padx=10, pady=10)

        register_button = tk.Button(self, text="Register", command= partial(self.open_window, username_entry, password_entry))
        register_button.grid(column=2, row=2, padx=10, pady=10)

    # def create_database(self):
    #     if os.path.exists("COM534.db"):
    #         db = Database("COM534.db")
    #         queries = ["CREATE TABLE People ([People ID] INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, Forename TEXT, Surname TEXT, [Address ID] INTEGER REFERENCES Address ([Address ID]), [Phone Number] INTEGER, Email TEXT, [Branch ID] INTEGER REFERENCES Branch ([Branch ID]));"]
    def login(self,username,password):
        username = username.get()
        password = password.get()
        db = Database("login.db")
        query ="""
        SELECT * FROM Login WHERE Username = ?;
        """
        results = db.cursor.execute(query, (username,)).fetchone()
        print (results)
        if results is not None:
            cipher = Fernet(results[3])

            if results[1] ==  username and cipher.decrypt(results[2]).decode() == password:
                messagebox.showinfo("Information", "Login Successful")
        else:
            messagebox.showerror("Error", "Login Failed, no such user")

        db.connection.commit()
        db.disconnect()

    def open_window(self, username, password):
        window = Register(self, username, password)
        window.grab_set()
        self.withdraw()




class Register(tk.Toplevel):
    def __init__(self, parent, username_entry, password_entry):
        super().__init__(parent)
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

        branch_dropdown = ttk.Combobox(self, values=branches, textvariable=branch, state="readonly")
        branch_dropdown.grid(column=1, row=8, padx=10, pady=10)














main = Main()
main.mainloop()