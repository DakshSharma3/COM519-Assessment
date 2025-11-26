# tkinter_app/main.py

import tkinter as tk
from tkinter import messagebox
from functools import partial
from tkinter import ttk
from cryptography.fernet import Fernet

from main_menu import MainMenu
from register import Register
from database import Database
import os

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        #When using work laptop use C:\\Users\\e465565\\Desktop\\Git Repos\\COM519\\COM519-Assessment\\com519\\src\\com519\\COM519.db
        self.database_name = "COM519.db"
        self.create_database()
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

        register_button = tk.Button(self, text="Register", command= partial(self.open_register_window, username_entry, password_entry))
        register_button.grid(column=2, row=2, padx=10, pady=10)

    def create_database(self):
        """Created the database if the .db file isn't present on startup"""
        if not os.path.exists(self.database_name):
            db = Database(self.database_name)
            db.create_tables()
            db.disconnect()

    def login(self,username,password):
        """
        validates the data inputted by the user by doing a lookup in the database and decrypting the password. If successful then the user is logged into the application.

        Args:
            username: username inputted by the user in the GUI
            password: password inputted by the user in the GUI
        """
        username = username.get()
        password = password.get()
        db = Database(self.database_name)
        query ="""
        SELECT * FROM Login WHERE Username = ?;
        """
        results = db.cursor.execute(query, (username,)).fetchone()
        print (results)
        if results is not None:
            cipher = Fernet(results[3])

            if results[1] ==  username and cipher.decrypt(results[2]).decode() == password:
                self.open_menu_window(db.get_user_id(username))
        else:
            messagebox.showerror("Error", "Login Failed, no such user")

        db.disconnect()

    def open_register_window(self, username, password):
        """
        Opens the register window

        Args:
            username: username inputted by the user in the GUI
            password: password inputted by the user in the GUI
        """
        window = Register(self, username, password)
        window.protocol("WM_DELETE_WINDOW", window.on_closing)
        window.grab_set()
        self.withdraw()

    def open_menu_window(self, user_id):
        """
        Opens the main meny window

        Args:
            user_id: ID of the logged-in user
        """
        window = MainMenu(self, user_id)
        window.protocol("WM_DELETE_WINDOW", window.on_closing)
        window.grab_set()
        self.withdraw()

    def on_closing(self):
        """Closes the application"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            exit()

main = Main()
main.protocol("WM_DELETE_WINDOW", main.on_closing)
main.mainloop()