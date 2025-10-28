# tkinter_app/main.py

import tkinter as tk
from tkinter import messagebox
from functools import partial
from database import Database


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
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

        login_button = tk.Button(self, text="Login", command= partial(login, username_entry, password_entry))
        login_button.grid(column=0, row=2, padx=10, pady=10)

        register_button = tk.Button(self, text="Register", command= partial(register, username_entry, password_entry))
        register_button.grid(column=2, row=2, padx=10, pady=10)



def login(username,password):
    username = username.get()
    password = password.get()
    db = Database("login.db")
    query ="""
    SELECT * FROM Login WHERE Username = ? AND Password = ?;
    """
    results = db.cursor.execute(query, (username,password)).fetchone()
    if results is not None:
        if results[1] ==  username and results[2]  == password:
            messagebox.showinfo("Information", "Login Successful")
    else:
        messagebox.showerror("Error", "Login Failed, no such user")

    db.connection.commit()
    db.disconnect()

def valid_username(username, db):
    query = """SELECT * FROM Login WHERE Username = ?;
    """
    results = db.cursor.execute(query, (username,)).fetchall()
    print(len(results))
    if len(results) <= 0:
        return True
    else:
        return False

def valid_password(password, db):
    valid_length = len(password) >= 8
    has_digit = any(character.isdigit() for character in password)
    has_uppercase = any(character.isupper() for character in password)
    has_symbol = any(character.isalnum() for character in password)

    if valid_length and has_digit and has_uppercase and has_symbol:
        return True
    else:
        return False



def register(username, password):
    username = username.get()
    password = password.get()
    db = Database("login.db")
    if valid_username(username, db):
        if valid_password(password, db):
            query = """
            INSERT INTO Login (Username, Password) VALUES (?, ?);
            """
            db.cursor.execute(query, (username, password))
            db.connection.commit()
            messagebox.showinfo("Information", "Registration Successful")
            db.disconnect()
        else:
            messagebox.showerror("Error", "Registration Failed, password does not meet requirements\n\n- 8 or more characters\n- Contains a capital letter\n- Contains a number\n- Contains a special character")
            db.disconnect()
    else:
        messagebox.showerror("Error", "Registration Failed, username may already exist")
        db.disconnect()

        # Add your username validation logic here


main = Main()
main.mainloop()