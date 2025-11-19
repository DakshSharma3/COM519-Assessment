import tkinter as tk
from functools import partial
from tkinter import ttk, messagebox

from cryptography.fernet import Fernet

from database import Database


class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.database_name = "COM519.db"
        self.title("Main Menu")
        self.geometry("300x300")
        self.db = Database(self.database_name)
        for i in range (0,2):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(0, weight=2)
        for i in range (1,3):
            self.rowconfigure(i, weight=1)
        for r in range(3):
            for c in range(2):
                frame = tk.Frame(self, bd=1, relief="solid")  # outline
                frame.grid(row=r, column=c, sticky="nsew")

        username_text = tk.Label(self, text="Main Menu", font=("Arial", 16))
        username_text.grid(column=1, row=0, padx=10, pady=10, columnspan=2)

        add_account_button = tk.Button(self, text="Add Account")
        add_account_button.grid(column=0, row=1, padx=10, pady=10)

        view_account_button = tk.Button(self, text="View Account")
        view_account_button.grid(column=1, row=1, padx=10, pady=10)

        add_appointment_button = tk.Button(self, text="Add Appointment")
        add_appointment_button.grid(column=0, row=2, padx=10, pady=10)

        view_appointment_button = tk.Button(self, text="View Appointment")
        view_appointment_button.grid(column=1, row=2, padx=10, pady=10)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

main = MainMenu()
main.protocol("WM_DELETE_WINDOW", main.on_closing)
main.mainloop()