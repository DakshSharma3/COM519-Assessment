# tkinter_app/main.py

import sqlite3
import tkinter as tk
from tkinter import messagebox
from functools import partial


def login(username,password):
    username = username.get()
    password = password.get()
    con = sqlite3.connect("C:/Users/e465565/Desktop/Git Repos/COM519/COM519-Assessment/com519/src/com519/login.db")
    cursor = con.cursor()
    query ="""
    SELECT * FROM Login WHERE Username = ? AND Password = ?;
    """
    results = cursor.execute(query, (username,password)).fetchone()

    if results[1] ==  username and results[2] == password:
        messagebox.showinfo("Information", "Login Successful")
    else:
        messagebox.showerror("Error", "Login Failed")

    con.commit()
    # messagebox.showinfo("Information", f"{results}")


def main():
    root = tk.Tk()
    root.title("My Tkinter App")
    root.geometry("400x150")
    username = tk.StringVar()
    password = tk.StringVar()


    usernameText = tk.Label(root, text="Username: ", font=("Arial", 16))
    usernameText.grid(column=0, row=0, padx=10, pady=10)

    usernameEntry = tk.Entry(root, textvariable=username)
    usernameEntry.grid(column=1, row=0, padx=10, pady=10)


    passwordText = tk.Label(root, text="Password: ", font=("Arial", 16))
    passwordText.grid(column=0, row=1, padx=10, pady=10)



    passwordEntry = tk.Entry(root, textvariable=password, show="*")
    passwordEntry.grid(column=1, row=1, padx=10, pady=10)

    loginButton = tk.Button(root, text="Login", command= partial(login, usernameEntry, passwordEntry))
    loginButton.grid(column=1, row=2, padx=10, pady=10)




    root.mainloop()

if __name__ == "__main__":
    main()


# con = sqlite3.connect("C:/Users/e465565/Desktop/Git Repos/COM519/COM519-Assessment/com519/src/com519/login.db")
# cursor = con.cursor()
# """
# CREATE TABLE Login (
#     UserID INTEGER PRIMARY KEY AUTOINCREMENT,
#     Username Text,
#     Password Text
# );
# """ 
# """
# INSERT INTO Login (Username, Password) VALUES
# ('admin', 'password123');
# """ 


# query ="""
# SELECT * FROM Login;
# """

# results = cursor.execute(query).fetchall()
# con.commit() 
# print(results)

# con.close()