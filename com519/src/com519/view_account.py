import tkinter as tk
from tkinter import messagebox
from database import Database


class ViewAccount(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.parent = parent
        self.user = user
        self.database_name = "COM519.db"
        self.title("My Tkinter App")
        self.geometry("450x400")
        self.account_type = tk.StringVar()
        self.specific_account_type = tk.StringVar()
        self.balance = tk.StringVar()
        self.db = Database(self.database_name)
        self.accounts = self.db.get_all_user_bank_accounts(self.user.get_people_id())
        self.selected_account = None

        for i in range (0,4):
            self.rowconfigure(i, weight=1)
        for i in range (0,4):
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

        self.available_account_listbox.grid(column=0, row=1, padx=10, columnspan=2, rowspan=2)
        print(self.accounts[1])
        for account in self.accounts:
            self.available_account_listbox.insert(tk.END, account[2])

        account_type_text = tk.Label(self, text="Account Type: ", font=("Arial", 12))
        account_type_text.grid(column=2, row=1, padx=10, pady=10)

        self.account_type_entry = tk.Entry(self, textvariable=self.specific_account_type)
        self.account_type_entry.grid(column=3, row=1, padx=10, pady=10)

        balance_text = tk.Label(self, text="Balance: ", font=("Arial", 12))
        balance_text.grid(column=2, row=2, padx=10, pady=10, sticky="w")

        self.balance_entry = tk.Entry(self, textvariable=self.balance)
        self.balance_entry.grid(column=3, row=2, padx=10, pady=10, sticky="w")

        self.confirm_balance_button = tk.Button(self, text="Confirm balance", command=self.change_balance)

    def action(self, event):
        selection = self.available_account_listbox.curselection()[0]
        self.confirm_balance_button.grid_forget()
        self.selected_account = self.accounts[selection]
        self.fill_selected_account_list()
        change_balance_button = tk.Button(self, text="Change balance", command=self.changing_balance)
        change_balance_button.grid(column=0, row=3, padx=10, pady=10, columnspan=2)


    def fill_selected_account_list(self):
        self.account_type_entry.config(state=tk.NORMAL)
        self.balance_entry.config(state=tk.NORMAL)
        self.account_type_entry.delete(0, tk.END)
        self.account_type_entry.insert(tk.END, self.selected_account[2])
        self.account_type_entry.config(state=tk.DISABLED)
        self.balance_entry.delete(0, tk.END)
        self.balance_entry.insert(tk.END, self.selected_account[3])
        self.balance_entry.config(state=tk.DISABLED)


    def on_closing(self):
        """Closes the application"""
        self.parent.update()
        self.parent.deiconify()
        self.destroy()

    def changing_balance(self):
        self.balance_entry.config(state=tk.NORMAL)
        self.confirm_balance_button.grid(column=2, row=3, padx=10, pady=10, columnspan=2)

    def change_balance(self):
        try:
            new_balance = float(self.balance_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid balance value")
            return False
        self.db.update_bank_balance(self.selected_account[0], new_balance)
        self.accounts = self.db.get_all_user_bank_accounts(self.user.get_people_id())
        self.confirm_balance_button.grid_forget()
        self.balance_entry.config(state=tk.DISABLED)
        return True


