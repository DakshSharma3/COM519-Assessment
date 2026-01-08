import tkinter as tk
from tkinter import ttk, messagebox

from database import Database
from datetime import date, time, datetime
import os
import xml.etree.cElementTree as ET


class AddAppointment(tk.Toplevel):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.parent = parent
        self.database_name = "C:\\Users\\e465565\\Desktop\\Git Repos\\COM519\\COM519-Assessment\\com519\\src\\com519\\COM519.db"
        self.title("Adding appointment")
        self.geometry("350x500")
        self.db = Database(self.database_name)
        self.user = user
        self.appointments_file_name = "C:\\Users\\e465565\\Desktop\\Git Repos\\COM519\\COM519-Assessment\\com519\\src\\com519\\appointments.xml"
        self.selected = tk.StringVar(value="")
        self.employee = tk.StringVar()
        self.customer = tk.StringVar()
        self.date = tk.StringVar()
        self.time = tk.StringVar()
        self.branch = tk.StringVar()
        self.purpose = tk.StringVar()
        username_text = tk.Label(self, text="Are you going to be the employee or customer?", font=("Arial", 12))
        username_text.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        tk.Radiobutton(self, text = "Employee", variable = self.selected, value = "Employee", command=self.on_selection).grid(column=0, row=1, padx=10, pady=10)

        tk.Radiobutton(self, text = "Customer", variable = self.selected, value = "Customer", command=self.on_selection).grid(column=1, row=1, padx=10, pady=10)


        customer_text = tk.Label(self, text="Customer: ", font=("Arial", 16))
        customer_text.grid(column=0, row=2, padx=10, pady=10)

        self.customer_dropdown = ttk.Combobox(self, values=self.db.get_all_customer_names(), textvariable=self.customer, state="readonly")
        self.customer_dropdown.grid(column=1, row=2, padx=10, pady=10)

        employee_text = tk.Label(self, text="Employee: ", font=("Arial", 16))
        employee_text.grid(column=0, row=3, padx=10, pady=10)

        self.employee_dropdown = ttk.Combobox(self, values=self.db.get_all_employee_names(), textvariable=self.employee, state="readonly")
        self.employee_dropdown.grid(column=1, row=3, padx=10, pady=10)

        date_text = tk.Label(self, text="Date: ", font=("Arial", 16))
        date_text.grid(column=0, row=4, padx=10, pady=10)

        date_entry = tk.Entry(self, textvariable=self.date)
        date_entry.grid(column=1, row=4, padx=10, pady=10)

        time_text = tk.Label(self, text="Time: ", font=("Arial", 16))
        time_text.grid(column=0, row=5, padx=10, pady=10)

        time_entry = tk.Entry(self, textvariable=self.time)
        time_entry.grid(column=1, row=5, padx=10, pady=10)

        branch_text = tk.Label(self, text="Branch: ", font=("Arial", 16))
        branch_text.grid(column=0, row=6, padx=10, pady=10)

        branch_dropdown = ttk.Combobox(self, values=self.db.get_branch_names(), textvariable=self.branch, state="readonly")
        branch_dropdown.grid(column=1, row=6, padx=10, pady=10)

        purpose_text = tk.Label(self, text="Purpose: ", font=("Arial", 16))
        purpose_text.grid(column=0, row=7, padx=10, pady=10)

        purpose_entry = tk.Entry(self, textvariable=self.purpose)
        purpose_entry.grid(column=1, row=7, padx=10, pady=10)

        add_appointment_button = tk.Button(self, text="Register", command=self.add_appointment)
        add_appointment_button.grid(column=1, row=8, padx=10, pady=10)


    def on_closing(self):
        """Returns the user to the main menu when closing the page"""
        self.db.disconnect()
        self.parent.update()
        self.parent.deiconify()
        self.destroy()

    def on_selection(self):
        if self.selected.get() == "Employee":
            if self.user.get_employee_id() is not None:
                self.employee_dropdown.set(f"{self.user.get_employee_id()} {self.user.get_forename()} {self.user.get_surname()}")
                self.employee_dropdown.config(state = "disabled")
                self.customer_dropdown.config(state = "readonly")
                self.customer_dropdown.set("")
        elif self.selected.get() == "Customer":
            if self.user.get_people_id() is not None:
                self.customer_dropdown.set(f"{self.user.get_people_id()} {self.user.get_forename()} {self.user.get_surname()}")
                self.customer_dropdown.config(state = "disabled")
                self.employee_dropdown.config(state = "readonly")
                self.employee_dropdown.set("")

    def add_appointment(self):
        if self.validate_date_time():
            if not os.path.exists(self.appointments_file_name):
                self.create_appointment_xml(self.appointments_file_name)
            self.add_to_xml(self.appointments_file_name)
            messagebox.showinfo("Success", "Appointment successfully registered!")
        else:
            messagebox.showerror("Error", "Invalid Date Time\n-Date should be in DD/MM/YYYY format\n-Time should be in HH:MM format")

    def validate_date_time(self):
        try:
            datetime.strptime(self.date.get(), "%d/%m/%Y")
            datetime.strptime(self.time.get(), "%H:%M")
            return True

        except ValueError:
            return False

    def create_appointment_xml(self, file_name):
        root = ET.Element("Appointments")
        tree = ET.ElementTree(root)
        tree.write(file_name, encoding="utf-8", xml_declaration=True)

    def add_to_xml(self, file_name):
        
        tree = ET.parse(file_name)
        root = tree.getroot()

        new_id = 0
        for appt in root.findall("appointment"):
            appt_id = int(appt.get("id", 0))
            new_id = max(new_id, appt_id)

        new_id += 1

        doc = ET.SubElement(root, "appointment", id = str(new_id))

        ET.SubElement(doc, "employee_id").text = self.employee.get().split(" ")[0]
        ET.SubElement(doc, "people_id").text = self.customer.get().split(" ")[0]
        ET.SubElement(doc, "branch_id").text = str(self.db.get_branch_id(self.branch.get()))
        ET.SubElement(doc, "date").text = self.date.get()
        ET.SubElement(doc, "time").text = self.time.get()
        ET.SubElement(doc, "purpose").text = self.purpose.get()
        ET.indent(root, space="    ", level=0)
        tree = ET.ElementTree(root)

        tree.write(file_name, encoding="utf-8", xml_declaration=True)