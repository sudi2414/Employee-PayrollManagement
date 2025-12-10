import mysql.connector
from mysql.connector import Error
class DBconnect:
    #connection to the database
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                passwd = "Sarma@09112006",
                database = "employee_sys",
                autocommit = True
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("Database connection established")
        except Error as e:
            print("Database connection failed",e)

    #simple query execution
    def execute(self, query,parameters = None):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(query, parameters)
        return cursor
    #employee login
    def login_check(self,email,password):
        #employee login
        sql  = "SELECT * FROM employees WHERE email = %s AND emp_pass=%s"
        self.cursor.execute(sql,(email,password))
        emp = self.cursor.fetchone()
        if emp:
            return ("employee" , emp)
        sql = "SELECT * FROM hr_admin WHERE username = %s AND pass = %s"
        self.cursor.execute(sql,(email,password))
        hr = self.cursor.fetchone()
        if hr:
            return ("hr",hr)
        return None

    ##fetching employee details

    def employee_details(self,emp_id):
        sql = """SELECT e.*,d.department_name
         FROM employees e
         JOIN departments d ON e.department_id = d.department_id
         WHERE e.emp_id = %s"""
        self.cursor.execute(sql,(emp_id,))
        return self.cursor.fetchone()

    ## getting all employees

    def all_employees(self):
        sql = "SELECT e.*,d.department_name FROM employees e JOIN departments d ON e.department_id = d.department_id"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    ## add employee

    def add_employee(self,emp_name,department_id,designation,base_salary,join_date,email,phone,emp_pass):
        sql = """
        INSERT INTO employees 
        (emp_name,department_id,designation,base_salary,join_date,email,phone,emp_pass) 
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s) 
        """
        params = (emp_name,department_id,designation,base_salary,join_date,email,phone,emp_pass)
        self.cursor.execute(sql,params)

    ## deleting an employee
    def delete_employee(self,emp_id ):
        sql = "DELETE FROM employees WHERE emp_id = %s"
        self.cursor.execute(sql,(emp_id,))

    ## updation of an employee

    def update_employee(self,emp_id,emp_name,department_id,designation,base_salary,join_date,email,phone,emp_pass):
        sql = """
        UPDATE employees SET emp_name=%s,
        department_id=%s,
        designation=%s,
        base_salary=%s,
        join_date=%s,
        email=%s,
        phone=%s,
        emp_pass=%s 
        WHERE emp_id=%s"""
        params = (emp_name,department_id,designation,base_salary,join_date,email,phone,emp_pass,emp_id)
        self.cursor.execute(sql,params)

    ### applying a leave

    def apply_leave(self,emp_id,start_date,end_date,reason):
        sql = """
        INSERT INTO leave_management (emp_id,start_date,end_date,reason,stat)
        VALUES (%s,%s,%s,%s,'pending')"""
        self.cursor.execute(sql,(emp_id,start_date,end_date,reason))

    ### updating leave status (by hr)

    def update_leave_status(self,leave_id,stat):
        sql = """
        UPDATE leave_management SET  stat = %s WHERE leave_id = %s
        """
        self.cursor.execute(sql,(stat,leave_id))
        self.conn.commit()

    ## employee attandance marking

    def mark_attendance(self,emp_id,status):
        sql = """INSERT INTO attandance (emp_id,date_att,stat) 
        VALUES (%s,CURDATE(),%s)"""
        self.cursor.execute(sql,(emp_id,status))
        self.conn.commit()

    ## getting the payroll

    def add_payroll(self,emp_id,month,basic,hra,deductions,net_salary):
        sql = """
        INSERT INTO payroll (emp_id,month_nam,basic,hra,deductions,net_salary,generated_on) 
        VALUES (%s,%s, %s, %s, %s, %s,CURDATE())
        """
        params = (emp_id,month,basic,hra,deductions,net_salary)
        self.cursor.execute(sql,params)
        self.conn.commit()

    def attandance_for_date(self,emp_id,date):
        sql = "SELECT *  FROM attandance WHERE date_att = %s and emp_id = %s"
        params = (date,emp_id)
        self.cursor.execute(sql,params)
        return self.cursor.fetchone()

    def get_pending_leaves(self):
        sql = """
        SELECT l.*,e.emp_name,e.email
        FROM leave_management l
        JOIN employees e ON l.emp_id = e.emp_id
        where l.stat = 'pending'
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def count_absent_days_in_month(self, emp_id, year, month):
        sql = """
        SELECT COUNT(*) AS cnt 
        FROM attandance 
        WHERE emp_id=%s 
          AND YEAR(date_att)=%s 
          AND MONTH(date_att)=%s 
          AND stat='absent'
        """
        self.cursor.execute(sql, (emp_id, year, month))
        row = self.cursor.fetchone()
        return row['cnt'] if row else 0

    def get_payroll(self, emp_id, month_nam):
        sql = "SELECT * FROM payroll WHERE emp_id=%s AND month_nam=%s"
        self.cursor.execute(sql, (emp_id, month_nam))
        return self.cursor.fetchone()

    #getting attandance summary today

    def get_attandance_summary_today(self,date_obj):
        sql = "SELECT stat,count(*) AS cnt FROM attandance WHERE date_att = %s GROUP BY stat"
        self.cursor.execute(sql,(date_obj,))
        return self.cursor.fetchall()


    def get_departmentwise_attandance_today(self,date_obj):
        sql = """
        SELECT d.department_name,
            SUM(CASE WHEN a.stat = 'present' THEN 1 ELSE 0 END) AS present_count,
            SUM(CASE WHEN a.stat = 'absent' THEN 1 ELSE 0 END) AS absent_count,
            SUM(CASE WHEN a.stat = 'leave' THEN 1 ELSE 0 END) AS leave_count
        FROM attandance a 
        JOIN employees e ON a.emp_id = e.emp_id
        LEFT JOIN departments d ON e.department_id = d.department_id
        WHERE a.date_att = %s
        GROUP BY d.department_name
        """
        self.cursor.execute(sql,(date_obj,))
        return self.cursor.fetchall()

    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            self.conn = None
            print("DB connection closed")

