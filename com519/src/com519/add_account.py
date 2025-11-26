import tkinter as tk
from functools import partial
from tkinter import ttk, messagebox

from cryptography.fernet import Fernet

from database import Database


class AddAccount(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.database_name = "COM519.db"
        self.title("My Tkinter App")
        self.geometry("350x200")
        account_type = tk.StringVar()
        self.db = Database(self.database_name)

        for i in range (0,3):
            self.rowconfigure(i, weight=1)
        for i in range (0,2):
            self.columnconfigure(i, weight=1)

        main_menu_text = tk.Label(self, text="Add Account", font=("Arial", 16))
        main_menu_text.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        account_type_text = tk.Label(self, text="Account Type: ", font=("Arial", 16))
        account_type_text.grid(column=0, row=1, padx=10)

        account_type_dropdown = ttk.Combobox(self, values=self.db.get_account_type_names(), textvariable=account_type, state="readonly")
        account_type_dropdown.grid(column=1, row=1, padx=10)

        register_button = tk.Button(self, text="Register Account" )
        register_button.grid(column=0, row=2, padx=10, pady=10, columnspan=2)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            exit()

    def register_account(self, account_type):
        account_type_id = self.db.get_account_type_id(account_type)
        if account_type_id != None:
            self.db.register_account(account_type)


