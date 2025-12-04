import tkinter as tk
from functools import partial
from tkinter import ttk, messagebox

from cryptography.fernet import Fernet

from database import Database


class ViewAccount(tk.Toplevel):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.user_id = user_id
        self.database_name = "COM519.db"
        self.title("My Tkinter App")
        self.geometry("350x400")
        self.account_type = tk.StringVar()
        self.db = Database(self.database_name)

        for i in range (0,3):
            self.rowconfigure(i, weight=1)
        for i in range (0,2):
            self.columnconfigure(i, weight=1)

        main_menu_text = tk.Label(self, text="View Account", font=("Arial", 16))
        main_menu_text.grid(column=0, row=0, padx=10, pady=10)

        available_account_listbox = tk.Listbox(self, height=10,
                             width=15,
                             bg="grey",
                             activestyle='dotbox',
                             font="Helvetica",
                             fg="yellow",
                             listvariable=self.account_type,
                             selectmode="single")
        available_account_listbox.bind('<<ListboxSelect>>', self.action())

        available_account_listbox.grid(column=0, row=1, padx=10)
        for account in self.db.get_all_user_bank_accounts(user_id):
            available_account_listbox.insert(tk.END, account[1])

        specific_account_listbox = tk.Listbox(self, height=10,
                             width=15,
                             bg="grey",
                             activestyle='dotbox',
                             font="Helvetica",
                             fg="yellow")

        register_button = tk.Button(self, text="Register Account")
        register_button.grid(column=0, row=2, padx=10, pady=10, columnspan=2)


    def action(self):
        print(self.account_type)

    def on_closing(self):
        """Closes the application"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            exit()


