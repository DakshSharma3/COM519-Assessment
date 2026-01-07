import tkinter as tk
from functools import partial
from tkinter import ttk, messagebox, filedialog
from add_account import AddAccount
from view_account import ViewAccount
from database import Database


class UpdateProfilePicture(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.parent = parent
        self.database_name = "COM519.db"
        self.title("Update Profile in picture")
        self.geometry("300x300")
        self.db = Database(self.database_name)
        self.user = user

        tk.Button(self, text="Upload PNG File", command=upload_file).pack(pady=20)

    def on_closing(self):
        """Returns the user to the main menu when closing the page"""
        self.db.disconnect()
        self.parent.update()
        self.parent.deiconify()
        self.destroy()

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

    def logout(self):
        """Logs the user out and returns them to the login page"""
        self.db.disconnect()
        self.parent.update()
        self.parent.deiconify()
        self.destroy()


def upload_file():
    file_path = filedialog.askopenfilename(
        title="Upload PNG File",
        filetypes=[("PNG files", "*.png")]
    )
    with open(file_path, 'rb') as file:
        file_blob = file.read()
        print(file_blob)

# main = MainMenu()
# main.protocol("WM_DELETE_WINDOW", main.on_closing)
# main.mainloop()