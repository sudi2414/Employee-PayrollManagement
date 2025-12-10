import customtkinter as ctk
from tkinter import messagebox
from dbconnect import DBconnect
from employee_dashboard import EmployeeDashboard
from hr_dashboard import HRDashboard

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = DBconnect()

        self.title("Employee Management System - Login")
        self.geometry("450x350")
        ctk.set_appearance_mode("light")

        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        title = ctk.CTkLabel(frame, text="Login", font=("Arial", 26, "bold"))
        title.pack(pady=20)

        # Email / Username Entry
        self.email_entry = ctk.CTkEntry(frame, placeholder_text="Email / Username")
        self.email_entry.pack(pady=10, padx=20)

        # Password Entry
        self.pass_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
        self.pass_entry.pack(pady=10, padx=20)

        # Login Button
        login_btn = ctk.CTkButton(frame, text="Login", command=self.do_login)
        login_btn.pack(pady=20)

    def do_login(self):
        email = self.email_entry.get()
        password = self.pass_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return

        result = self.db.login_check(email, password)

        if not result:
            messagebox.showerror("Error", "Invalid Login Credentials")
            return

        role, data = result
        # ------------------------------ EMPLOYEE -----------------------------
        if role == "employee":
            messagebox.showinfo("Success", "Employee Login Successful")
            self.destroy()
            emp_screen = EmployeeDashboard(data)
            emp_screen.mainloop()
            return

        # ------------------------------ HR ADMIN -----------------------------
        elif role == "hr":
            messagebox.showinfo("Success", "HR Login Successful")
            self.destroy()

            #This is where HR view will be opened
            hr_screen = HRDashboard(data)
            hr_screen.mainloop()
        else:
            messagebox.showerror("Error", "Unknown user type")


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
