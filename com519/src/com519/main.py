# tkinter_app/main.py

import tkinter as tk
from tkinter import messagebox
from functools import partial
from tkinter import ttk
from cryptography.fernet import Fernet

from com519.register import Register
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
        db = Database("COM519.db")
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



main = Main()
main.mainloop()