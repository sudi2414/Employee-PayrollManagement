import customtkinter as ct
from tkinter import messagebox
import tkinter as tk
from datetime import datetime,date
import matplotlib.pyplot as plt

from dbconnect import DBconnect

class HRDashboard(ct.CTk):
    def __init__(self,hr_data):
        super().__init__()

        self.db = DBconnect()
        self.hr = hr_data

        self.title("HR Dashboard")
        self.geometry("1100x650")
        ct.set_appearance_mode("light")

        sidebar = ct.CTkFrame(self,width = 200)
        sidebar.pack(side="left",fill="y")

        btn1 = ct.CTkButton(sidebar, text="Manage Employees", command=self.show_employee_management)
        btn1.pack(pady=20)

        btn2 = ct.CTkButton(sidebar, text="Approve Leaves", command=self.show_leave_approval)
        btn2.pack(pady=20)

        btn3 = ct.CTkButton(sidebar, text="Generate Payroll", command=self.show_payroll)
        btn3.pack(pady=20)

        btn4 = ct.CTkButton(sidebar, text="Analytics", command=self.show_analytics)
        btn4.pack(pady=20)

        self.content = ct.CTkFrame(self)
        self.content.pack(fill="both", expand=True)

        self.show_employee_management()

    def show_employee_management(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        title = ct.CTkLabel(self.content, text="Manage Employees", font=("Arial", 24, "bold"))
        title.pack(pady=10)

        # --- Form ---
        form_frame = ct.CTkFrame(self.content)
        form_frame.pack(pady=20)
        self.e_nam_lab = ct.CTkLabel(form_frame, text="Employee Name:")
        self.e_nam_lab.grid(row=0,column=0,padx=10,pady=5)

        self.e_name = ct.CTkEntry(form_frame, width=200, placeholder_text="Employee Name")
        self.e_name.grid(row=0, column=1, padx=10, pady=5)

        self.e_dep_lab = ct.CTkLabel(form_frame, text="Department ID:")
        self.e_dep_lab.grid(row=0, column=2, padx=10, pady=5)

        self.e_dep = ct.CTkEntry(form_frame, width=200, placeholder_text="Department ID")
        self.e_dep.grid(row=0, column=3, padx=10, pady=5)

        self.e_desi_lab = ct.CTkLabel(form_frame, text="Designation:")
        self.e_desi_lab.grid(row=1, column=0, padx=10, pady=5)

        self.e_desig = ct.CTkEntry(form_frame, width=200, placeholder_text="Designation")
        self.e_desig.grid(row=1, column=1, padx=10, pady=5)

        self.e_sal_lab = ct.CTkLabel(form_frame, text="Base Salary:")
        self.e_sal_lab.grid(row=1, column=2, padx=10, pady=5)

        self.e_salary = ct.CTkEntry(form_frame, width=200, placeholder_text="Base Salary")
        self.e_salary.grid(row=1, column=3, padx=10, pady=5)

        self.e_jo_lab = ct.CTkLabel(form_frame, text="Join date:")
        self.e_jo_lab.grid(row=2, column=0, padx=10, pady=5)

        self.e_join = ct.CTkEntry(form_frame, width=200, placeholder_text="Join Date (YYYY-MM-DD)")
        self.e_join.grid(row=2, column=1, padx=10, pady=5)

        self.e_em_lab = ct.CTkLabel(form_frame, text="Email:")
        self.e_em_lab.grid(row=2, column=2, padx=10, pady=5)

        self.e_email = ct.CTkEntry(form_frame, width=200, placeholder_text="Email")
        self.e_email.grid(row=2, column=3, padx=10, pady=5)

        self.e_ph_lab = ct.CTkLabel(form_frame, text="phone number:")
        self.e_ph_lab.grid(row=3, column=0, padx=10, pady=5)

        self.e_phone = ct.CTkEntry(form_frame, width=200, placeholder_text="Phone")
        self.e_phone.grid(row=3, column=1, padx=10, pady=5)

        self.e_pas_lab = ct.CTkLabel(form_frame, text="Password:")
        self.e_pas_lab.grid(row=3, column=2, padx=10, pady=5)

        self.e_pass = ct.CTkEntry(form_frame, width=200, placeholder_text="Password")
        self.e_pass.grid(row=3, column=3, padx=10, pady=5)

        # Buttons
        add_btn = ct.CTkButton(self.content, text="Add Employee", command=self.add_employee)
        add_btn.pack(pady=5)

        update_btn = ct.CTkButton(self.content, text="Update Employee", command=self.update_employee)
        update_btn.pack(pady=5)

        del_btn = ct.CTkButton(self.content, text="Delete Employee", command=self.delete_employee)
        del_btn.pack(pady=5)

        clr_btn = ct.CTkButton(self.content, text="clear", command=self.clr_det)
        clr_btn.pack(pady=5)
        # Employee List
        self.emp_list = tk.Listbox(self.content, width=140, height=12)
        self.emp_list.pack(pady=10)

        self.emp_list.bind('<<ListboxSelect>>', self.on_employee_select)

        self.load_employees()

    def load_employees(self):
        self.emp_list.delete(0, tk.END)
        data = self.db.all_employees()

        for row in data:
            self.emp_list.insert(tk.END,
                                 f"{row['emp_id']} | {row['emp_name']} | {row['department_name']} | {row['designation']}")

    def add_employee(self):
        try:
            number = self.e_phone.get()
            if len(number) ==10:
                self.db.add_employee(
                self.e_name.get(), self.e_dep.get(), self.e_desig.get(),
                self.e_salary.get(), self.e_join.get(), self.e_email.get(),
                self.e_phone.get(), self.e_pass.get()
                )
                messagebox.showinfo("Success", "Employee Added Successfully")
                self.load_employees()
            else:
                messagebox.showerror("Error", "Please enter a valid phone number")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_employee(self):
        try:
            selected = self.emp_list.get(tk.ACTIVE)
            emp_id = selected.split("|")[0].strip()

            self.db.update_employee(
                emp_id,
                self.e_name.get(), self.e_dep.get(), self.e_desig.get(),
                self.e_salary.get(), self.e_join.get(), self.e_email.get(),
                self.e_phone.get(), self.e_pass.get()
            )
            messagebox.showinfo("Success", "Employee Updated Successfully")
            self.load_employees()
        except:
            messagebox.showerror("Error", "Select an employee from the list")

    def delete_employee(self):
        try:
            selected = self.emp_list.get(tk.ACTIVE)
            emp_id = selected.split("|")[0].strip()

            self.db.delete_employee(emp_id)
            messagebox.showinfo("Success", "Employee Deleted Successfully")
            self.load_employees()
        except:
            messagebox.showerror("Error", "Select an employee first")

    def show_leave_approval(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        title = ct.CTkLabel(self.content, text="Approve Leave Requests", font=("Arial", 24, "bold"))
        title.pack(pady=10)

        query = "SELECT * FROM leave_management WHERE stat = 'pending'"
        cur = self.db.execute(query)
        leave_rows = cur.fetchall()

        self.leave_list = tk.Listbox(self.content, width=120, height=15)
        self.leave_list.pack(pady=10)

        for row in leave_rows:
            self.leave_list.insert(
                tk.END,
                f"{row['leave_id']} | {row['emp_id']} | "
                f"{row['start_date']} -> {row['end_date']} | {row['reason']}"
            )

        approve_btn = ct.CTkButton(
            master=self.content,
            text="Approve Leave",
            command=self.approve_leave
        )
        approve_btn.pack(pady=5)

        reject_btn = ct.CTkButton(
            master=self.content,
            text="Reject",
            command=self.reject_leave
        )
        reject_btn.pack(pady=5)


    def approve_leave(self):
        try:
            selected = self.leave_list.get(self.leave_list.curselection())
        except IndexError:
            messagebox.showerror("Error", "Please select a leave request.")
            return

        leave_id = selected.split("|")[0].strip()
        self.db.update_leave_status(leave_id, "approved")
        messagebox.showinfo("Success", "Leave Approved!")
        self.show_leave_approval()


    def reject_leave(self):
        try:
            selected = self.leave_list.get(self.leave_list.curselection())
        except IndexError:
            messagebox.showerror("Error", "Please select a leave request.")
            return

        leave_id = selected.split("|")[0].strip()
        self.db.update_leave_status(leave_id, "rejected")
        messagebox.showinfo("Success", "Leave Rejected!")

    def show_payroll(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        title = ct.CTkLabel(self.content, text="Generate Payroll", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        self.month_entry = ct.CTkEntry(self.content, placeholder_text="Enter Month Name (e.g., January)")
        self.month_entry.pack(pady=10)

        generate_btn = ct.CTkButton(self.content, text="Generate Payroll", command=self.generate_payroll)
        generate_btn.pack(pady=20)

    def generate_payroll(self):
        month = self.month_entry.get()
        year = datetime.now().year

        employees = self.db.all_employees()

        for emp in employees:
            emp_id = emp["emp_id"]
            basic = float(emp["base_salary"])
            hra = basic * 0.10  # 10% HRA

            absents = self.db.count_absent_days_in_month(emp_id, year, datetime.strptime(month, "%B").month)
            deductions = (basic / 30) * absents

            net_salary = basic + hra - deductions

            self.db.add_payroll(emp_id, month, basic, hra, deductions, net_salary)

        messagebox.showinfo("Success", "Payroll Generated Successfully!")

    def show_analytics(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        today = date.today()

        # PIE CHART
        stats = self.db.get_attandance_summary_today(today)
        labels = [row['stat'] for row in stats]
        values = [row['cnt'] for row in stats]

        plt.figure(figsize=(5, 5))
        plt.pie(values, labels=labels, autopct="%1.1f%%")
        plt.title("Today's Attendance Overview")
        plt.show()

        # BAR CHART
        dept_stats = self.db.get_departmentwise_attandance_today(today)
        deps = [row['department_name'] for row in dept_stats]
        present = [row['present_count'] for row in dept_stats]
        absent = [row['absent_count'] for row in dept_stats]
        leave = [row['leave_count'] for row in dept_stats]

        x = range(len(deps))
        plt.figure(figsize=(10, 5))
        plt.bar(x, present, label="Present")
        plt.bar(x, absent, bottom=present, label="Absent")
        plt.bar(x, leave, bottom=[present[i] + absent[i] for i in range(len(present))], label="Leave")

        plt.xticks(x, deps, rotation=45)
        plt.legend()
        plt.title("Department-wise Attendance")
        plt.show()

        # hr_dashboard.py (Add this new method to the class)

    def on_employee_select(self, event):
        try:
            # Get the index of the selected item
            selected_indices = self.emp_list.curselection()
            if not selected_indices:
                return

            # Get the full line of text for the selected item
            selected_text = self.emp_list.get(selected_indices[0])

            # Extract the emp_id (it's the first part before the first '|')
            emp_id = selected_text.split("|")[0].strip()

            # Fetch the complete details from the database
            employee_data = self.db.employee_details(emp_id)

            if employee_data:
                # Clear all entry fields first
                self.e_name.delete(0, 'end')
                self.e_dep.delete(0, 'end')
                self.e_desig.delete(0, 'end')
                self.e_salary.delete(0, 'end')
                self.e_join.delete(0, 'end')
                self.e_email.delete(0, 'end')
                self.e_phone.delete(0, 'end')
                self.e_pass.delete(0, 'end')

                # Insert the fetched data into the entry widgets
                self.e_name.insert(0, employee_data.get('emp_name', ''))
                self.e_dep.insert(0, employee_data.get('department_id', ''))  # Using dep_id for input
                self.e_desig.insert(0, employee_data.get('designation', ''))
                self.e_salary.insert(0, employee_data.get('base_salary', ''))
                self.e_join.insert(0, employee_data.get('join_date', ''))
                self.e_email.insert(0, employee_data.get('email', ''))
                self.e_phone.insert(0, employee_data.get('phone', ''))
                self.e_pass.insert(0, employee_data.get('emp_pass', ''))

        except Exception as e:
            # You can print the error for debugging, but don't show to user on selection
            print(f"Error loading employee details: {e}")

    def clr_det(self):
        self.e_name.delete(0, 'end')
        self.e_dep.delete(0, 'end')
        self.e_desig.delete(0, 'end')
        self.e_salary.delete(0, 'end')
        self.e_join.delete(0, 'end')
        self.e_email.delete(0, 'end')
        self.e_phone.delete(0, 'end')
        self.e_pass.delete(0, 'end')
        self.content.focus_set()