# tkinter_app/main.py

import tkinter as tk

def main():
    root = tk.Tk()
    root.title("My Tkinter App")
    root.geometry("300x200")

    label = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 16))
    label.pack(pady=50)

    root.mainloop()

if __name__ == "__main__":
    main()