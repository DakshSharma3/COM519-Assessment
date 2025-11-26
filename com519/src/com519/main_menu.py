import tkinter as tk
from functools import partial
from tkinter import ttk, messagebox

from cryptography.fernet import Fernet

from add_account import AddAccount
from database import Database


class MainMenu(tk.Toplevel):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.database_name = "COM519.db"
        self.title("Main Menu")
        self.geometry("300x300")
        self.db = Database(self.database_name)
        self.user_id = user_id

        for i in range (0,3):
            self.rowconfigure(i, weight=1)
        for i in range (0,2):
            self.columnconfigure(i, weight=1)

        main_menu_text = tk.Label(self, text="Main Menu", font=("Arial", 16))
        main_menu_text.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        add_account_button = tk.Button(self, text="Add Account", command= self.open_window)
        add_account_button.grid(column=0, row=1, padx=10, pady=10)

        view_account_button = tk.Button(self, text="View Account")
        view_account_button.grid(column=1, row=1, padx=10, pady=10)

        add_appointment_button = tk.Button(self, text="Add Appointment")
        add_appointment_button.grid(column=0, row=2, padx=10, pady=10)

        view_appointment_button = tk.Button(self, text="View Appointment")
        view_appointment_button.grid(column=1, row=2, padx=10, pady=10)

    def on_closing(self):
        """Closes the application"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            exit()

    def open_window(self):
        """ Opens the add account window """
        window = AddAccount(self)
        window.protocol("WM_DELETE_WINDOW", window.on_closing)
        window.grab_set()
        self.withdraw()


# main = MainMenu()
# main.protocol("WM_DELETE_WINDOW", main.on_closing)
# main.mainloop()