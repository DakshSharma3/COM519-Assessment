import tkinter as tk
from functools import partial
from tkinter import ttk, messagebox
from add_account import AddAccount
from view_account import ViewAccount
from database import Database


class MainMenu(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.database_name = "COM519.db"
        self.title("Main Menu")
        self.geometry("300x300")
        self.db = Database(self.database_name)
        self.user = user

        for i in range (0,3):
            self.rowconfigure(i, weight=1)
        for i in range (0,2):
            self.columnconfigure(i, weight=1)

        main_menu_text = tk.Label(self, text="Main Menu", font=("Arial", 16))
        main_menu_text.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        add_account_button = tk.Button(self, text="Add Account", command= partial(self.open_window, self.user, AddAccount))
        add_account_button.grid(column=0, row=1, padx=10, pady=10)

        view_account_button = tk.Button(self, text="View Account", command= partial(self.open_window, self.user, ViewAccount))
        view_account_button.grid(column=1, row=1, padx=10, pady=10)

        add_appointment_button = tk.Button(self, text="Add Appointment")
        add_appointment_button.grid(column=0, row=2, padx=10, pady=10)

        view_appointment_button = tk.Button(self, text="View Appointment")
        view_appointment_button.grid(column=1, row=2, padx=10, pady=10)

    def on_closing(self):
        """Closes the application"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.db.disconnect()
            exit()

    def open_window(self, user, window):
        """
        Opens a new window
        :param user: User object to use in the new window
        :param window: The type of window to open
        """
        window = window(self, user)
        window.protocol("WM_DELETE_WINDOW", window.on_closing)
        window.grab_set()
        self.withdraw()


# main = MainMenu()
# main.protocol("WM_DELETE_WINDOW", main.on_closing)
# main.mainloop()