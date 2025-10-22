# tkinter_app/main.py

import tkinter as tk
from tkinter import messagebox
from functools import partial


def login(username,password):
    username = username.get()
    password = password.get()
    messagebox.showinfo("Information", f"Usernmae is {username} and password is {password}")


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