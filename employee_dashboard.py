from dbconnect import DBconnect
import customtkinter as ct
from tkinter import messagebox
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tkinter as tk


class EmployeeDashboard(ct.CTk):
    def __init__(self, emp_data):
        super().__init__()
        self.db = DBconnect()
        self.emp = emp_data
        self.emp_id = emp_data['emp_id']

        self.title("Employee Dashboard")
        self.geometry("900x600")

        ct.set_appearance_mode("light")

        menu = ct.CTkFrame(self,width=200)
        menu.pack(side="left",fill="y")

        self.btn_home = ct.CTkButton(menu,text="home",command = self.show_home)
        self.btn_home.pack(pady=20)

        self.btn_leave = ct.CTkButton(menu,text="Apply Leave",command = self.leave_form)
        self.btn_leave.pack(pady=20)

        self.btn_salary = ct.CTkButton(menu,text="Download salary slip",command = self.show_salary_ui)
        self.btn_salary.pack(pady=20)

        self.content = ct.CTkFrame(self,corner_radius=15)
        self.content.pack(fill="both",expand=True,padx=10,pady=10)

        self.today_status = self.mark_attandance_auto()

        self.show_home()

    def mark_attandance_auto(self):
        today = datetime.today()
        row = self.db.attandance_for_date(self.emp_id, today)
        if row:
            return row['stat']
        now = datetime.now().time()
        cutoff = datetime.strptime("10:00", "%H:%M").time()

        if now <= cutoff:
            status = "present"
        else:
            q = """SELECT *FROM leave_management WHERE emp_id = %s 
            AND %s BETWEEN start_date and end_date
            AND stat = 'approved'
            """
            cur = self.db.execute(q, (self.emp_id, today))
            leave = cur.fetchone()
            if leave:
                status = "leave"
            else:
                status = "absent"
        self.db.mark_attendance(self.emp_id, status)
        return status
    def show_home(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        title = ct.CTkLabel(self.content,text = "welcome,"+self.emp["emp_name"],font=("arial",24,"bold"))
        title.pack(pady = 10)
        status_label = ct.CTkLabel(
            self.content,
            text=f"Today's Attendance Status: {self.today_status.upper()}",
            font=("arial",24,"bold")
        )
        status_label.pack(pady = 20)

    def leave_form(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        ct.CTkLabel(self.content,text = "apply leave",font=("arial",24,"bold")).pack(pady = 10)
        self.start_entry = ct.CTkEntry(self.content,placeholder_text = "Start Date(YYYY-MM-DD)")
        self.start_entry.pack(pady =10)
        self.end_entry = ct.CTkEntry(self.content, placeholder_text="End Date (YYYY-MM-DD)")
        self.end_entry.pack(pady=10)
        self.reason_entry = ct.CTkEntry(self.content, placeholder_text="Reason")
        self.reason_entry.pack(pady=10)
        submit = ct.CTkButton(self.content , text="Submit Leave Request",
                              command = self.apply_leave)
        submit.pack(pady=10)

        query = """
            SELECT * FROM leave_management WHERE emp_id = %s"""
        cur = self.db.execute(query, (self.emp_id,))
        leave = cur.fetchall()

        self.leave_list = tk.Listbox(self.content,width=200,height=15)
        self.leave_list.pack(pady=10)

        self.load_leaves(leave)

    def load_leaves(self,leave_list):
        self.leave_list.delete(0,tk.END)
        self.leave_list.insert(tk.END,f"leave_id | \t start_date | \t end_date | \t reason | \t status | ")
        for row in leave_list:
            self.leave_list.insert(tk.END,f"{row['leave_id']} | \t {row['start_date']} | \t {row['end_date']} | \t {row['reason']} | \t {row['stat']}")

    def apply_leave(self):
        start = self.start_entry.get()
        end = self.end_entry.get()
        reason = self.reason_entry.get()
        if not start or not end or not reason:
            messagebox.showerror("Error","Pls fill all the fields")
            return
        self.db.apply_leave(self.emp_id, start, end, reason)
        messagebox.showinfo("Success","Leave Request submitted")

    def show_salary_ui(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        ct.CTkLabel(self.content,text="Download Salary Slip",font=("arial",24,"bold")).pack(pady = 10)
        self.month_entry = ct.CTkEntry(self.content,placeholder_text="Month Name")
        self.month_entry.pack(pady=10)

        btn = ct.CTkButton(self.content, text="Download PDF",
                            command=self.generate_salary_pdf)
        btn.pack(pady=20)

    def generate_salary_pdf(self):
        month = self.month_entry.get()
        data = self.db.get_payroll(self.emp_id,month)
        if not data:
            messagebox.showerror("Error","Payroll not found for this month")
            return
        filename = f"salary_slip_{self.emp['emp_name']}_{month}.pdf"
        c = canvas.Canvas(filename,pagesize=letter)
        c.setFont("Helvetica",20)
        c.drawString(200,750,"Salary Slip")

        c.setFont("Helvetica",12)
        c.drawString(50, 700, f"Employee Name: {self.emp['emp_name']}")
        c.drawString(50, 680, f"Month: {month}")

        c.drawString(50, 640, f"Basic Salary: {data['basic']}")
        c.drawString(50, 620, f"HRA: {data['hra']}")
        c.drawString(50, 600, f"Deductions: {data['deductions']}")
        c.drawString(50, 580, f"Net Salary: {data['net_salary']}")

        c.save()

        messagebox.showinfo("Success", f"Salary Slip Saved:\n{filename}")