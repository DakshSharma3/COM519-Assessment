import tkinter as tk
from functools import partial
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet

from database import Database


class ViewAccount(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.database_name = "COM519.db"
        self.title("My Tkinter App")
        self.geometry("450x400")
        self.account_type = tk.StringVar()
        self.db = Database(self.database_name)
        self.accounts = self.db.get_all_user_bank_accounts(self.user.get_people_id())
        self.selected_account = None

        for i in range (0,3):
            self.rowconfigure(i, weight=1)
        for i in range (0,2):
            self.columnconfigure(i, weight=1)

        main_menu_text = tk.Label(self, text="View Account", font=("Arial", 16))
        main_menu_text.grid(column=0, row=0, padx=10, pady=10)

        self.available_account_listbox = tk.Listbox(self, height=10,
                             width=15,
                             bg="grey",
                             activestyle='dotbox',
                             font="Helvetica",
                             fg="yellow",
                             listvariable=self.account_type,
                             selectmode="single")
        self.available_account_listbox.bind('<<ListboxSelect>>', self.action)

        self.available_account_listbox.grid(column=0, row=1, padx=10)
        print(self.accounts[1])
        for account in self.accounts:
            self.available_account_listbox.insert(tk.END, account)

        self.specific_account_listbox = tk.Listbox(self, height=10,
                             width=22,
                             bg="white",
                             activestyle='dotbox',
                             font="Helvetica",
                             fg="yellow",
                             selectmode="browse")
        self.specific_account_listbox.grid(column=1, row=1, padx=10)

        register_button = tk.Button(self, text="Register Account")
        register_button.grid(column=0, row=2, padx=10, pady=10, columnspan=2)


    def action(self, event):
        # print("Account Type is " , self.available_account_listbox.get(self.available_account_listbox.curselection()))
        print("Account Type is ", self.available_account_listbox.curselection()[0])
        self.selected_account = self.available_account_listbox.get(self.available_account_listbox.curselection()[0])
        self.fill_selected_account_list()


    def fill_selected_account_list(self):
        self.specific_account_listbox.config(state="normal")
        self.specific_account_listbox.delete(0, tk.END)
        self.specific_account_listbox.insert(tk.END, f"Account Type: {self.selected_account[1]}")
        self.specific_account_listbox.insert(tk.END, "")
        self.specific_account_listbox.insert(tk.END, f"Account Balance: {self.selected_account[2]}")
        self.specific_account_listbox.config(state="disabled")


    def on_closing(self):
        """Closes the application"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            exit()


