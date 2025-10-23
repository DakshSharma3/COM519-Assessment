# tkinter_app/main.py

import sqlite3
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

        usernameText = tk.Label(self, text="Username: ", font=("Arial", 16))
        usernameText.grid(column=0, row=0, padx=10, pady=10)

        usernameEntry = tk.Entry(self, textvariable=username)
        usernameEntry.grid(column=1, row=0, padx=10, pady=10)


        passwordText = tk.Label(self, text="Password: ", font=("Arial", 16))
        passwordText.grid(column=0, row=1, padx=10, pady=10)


        passwordEntry = tk.Entry(self, textvariable=password, show="*")
        passwordEntry.grid(column=1, row=1, padx=10, pady=10)

        loginButton = tk.Button(self, text="Login", command= partial(login, usernameEntry, passwordEntry))
        loginButton.grid(column=0, row=2, padx=10, pady=10)

        registerButton = tk.Button(self, text="Register", command= partial(register, usernameEntry, passwordEntry))
        registerButton.grid(column=2, row=2, padx=10, pady=10)



def login(username,password):
    username = username.get()
    password = password.get()
    db = Database("C:/Users/e465565/Desktop/Git Repos/COM519/COM519-Assessment/com519/src/com519/login.db")
    query ="""
    SELECT * FROM Login WHERE Username = ? AND Password = ?;
    """
    results = db.cursor.execute(query, (username,password)).fetchone()
    if results is not None:
        if results[1] ==  username and results[2] == password:
            messagebox.showinfo("Information", "Login Successful")
    else:
        messagebox.showerror("Error", "Login Failed, no such user")

    db.connection.commit()
    db.disconnect()

def register(username, password):
    username = username.get()
    password = password.get()
    db = Database("C:/Users/e465565/Desktop/Git Repos/COM519/COM519-Assessment/com519/src/com519/login.db")
    validUsername(username, db)
    query = """
    INSERT INTO Login (Username, Password) VALUES (?, ?);
    """
    try:
        db.cursor.execute(query, (username, password))
        db.connection.commit()
        messagebox.showinfo("Information", "Registration Successful")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Registration Failed, username may already exist")


    def validUsername(username, db):
        query = """SELECT * FROM Login WHERE Username = ?;
        """
        results = db.cursor.execute(query, (username,)).fetchall()
        if len(results) >= 0:
            return True
        else:
            return False

        # Add your username validation logic here


    


main = Main()
main.mainloop()