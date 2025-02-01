import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from vereinskasse import *

class SystemGUI:
    def __init__(self):
        self.sys = System()
        self.root = None
        self.account = None
        self.sys.load_if_exists()
    def create_root(self):
        if self.root:
            self.root.destroy()
        self.root = tk.Tk()
        self.center_window(self.root)
    def center_window(self, window, width=400, height=300):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    def clear(self):
        """Clear all widgets from tk screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
    def start(self):
        self.login_gui()
        self.root.mainloop()
    def logout(self):
        self.account = None
        self.login_gui()
        self.sys.save_all()
    def try_create_department(self, name):
        if name == "":
            tk.Label(self.root, text="Invalid input.").grid(row=0,column=2, columnspan=2)
            return
        if self.sys.find_department(name) is not None:
            tk.Label(self.root, text="This department already exists.").grid(row=0, column=2,columnspan=2)
            return
        self.sys.create_department(name, 0)
        self.admin_gui()
    def new_department_gui(self):
        self.create_root()
        # all tk vars
        var_name = tk.StringVar()
        # entry field:
        tk.Entry(self.root, textvariable=var_name).grid(column=1,row=0)
        tk.Label(self.root, text="Department name").grid(column=0,row=0)
        tk.Button(self.root, text="Create Department", command=lambda: self.try_create_department(var_name.get())).grid(column=0, row=1)
        tk.Button(self.root, text="Cancel", command=self.admin_gui).grid(column=1,row=1)

    def try_create_account(self, name1, name2, password, acc_type, department_name):
        # check for empty fields
        invalid = False
        for s in [name1, name2, password, acc_type]:
            if s == "":
                invalid = True
                break
        department = None
        # check for department field if acctype is treasurer
        if acc_type == "treasurer":
            if department_name == "":
                invalid = True
            else:
                department = self.sys.find_department(department_name)
                if department is None:
                    invalid = True
        if invalid:  # output invalid input message
            tk.Label(self.root, text="Invalid input.").grid(column=0,row=6,columnspan=2)
            return
        if self.sys.find_account((name1, name2)) is not None:
            tk.Label(self.root, text="Account already exists.").grid(column=0, row=6, columnspan=2)
            return
        self.sys.create_account((name1, name2), password, acc_type, department)
        self.admin_gui()

    def try_money_operation(self, arg, amount, target):
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror(message="Invalid amount.")
            return
        if amount <= 0:
            messagebox.showerror(message="Amount must be greater than 0.")
            return
        d : Department = self.account.department
        if arg == 0:  # Deposit
            d.deposit(amount)
        elif arg == 1:  # Withdrawal
            if not d.withdrawal(amount):
                messagebox.showerror(message="Not enough money.")
                return
        elif arg == 2:  # Transfer
            target = self.sys.find_department(target)
            if target == None:
                messagebox.showerror(message="Invalid target department.")
                return
            if not d.transfer(amount, target):
                messagebox.showerror(message="Not enough money.")
                return
        messagebox.showinfo(message=f"Successfully {['deposited', 'withdrawn', 'transfered'][arg]} {str(amount)}$")
        self.treasurer_gui()
            

    def money_gui(self, arg):
        self.create_root()
        title = ["Deposit Money.", "Withdraw Money.", "Transfer Money."][arg]
        tk.Label(self.root, text=title).grid(row=0,column=0)
        
        var_amount = tk.StringVar()
        tk.Label(self.root, text="Amount:").grid(row=1,column=0)
        tk.Entry(self.root, textvariable=var_amount).grid(row=1,column=1)
        var_department = tk.StringVar()
        if arg == 2:
            department_names = [d.name for d in self.sys.departments]
            department_names.remove(self.account.department.name)  # remove own department
            department_names.append("")
            tk.OptionMenu(self.root, var_department, *department_names).grid(column=1, row=2)
        
        tk.Button(self.root, text="Execute", command = lambda: self.try_money_operation(arg, var_amount.get(), var_department.get())).grid(row=3,column=1)
        tk.Button(self.root, text="Cancel", command=self.treasurer_gui).grid(column=1, row=4)

    def new_account_gui(self):
        self.create_root()
        # all tk vars
        var_name1 = tk.StringVar()
        var_name2 = tk.StringVar()
        var_password = tk.StringVar()
        var_account_type = tk.StringVar()
        var_department_name = tk.StringVar()
        # tk entry fields
        tk.Entry(self.root, textvariable=var_name1).grid(column=1, row=0)
        tk.Entry(self.root, textvariable=var_name2).grid(column=1, row=1)
        tk.Entry(self.root, textvariable=var_password, show="*", bg="black", fg="white").grid(column=1, row=2)

        account_types = ["admin", "treasurer", "officer"]
        department_names = [d.name for d in self.sys.departments]
        department_names.append("")

        var_account_type.set(account_types[0])
        tk.OptionMenu(self.root, var_account_type, *account_types).grid(column=1,row=3)
        for i in range(5):
            tk.Label(self.root, text=(["First Name", "Last Name", "Password", "Account Type", "Department\n(for treasurers)"][i])).grid(column=0, row=i)
        tk.OptionMenu(self.root, var_department_name, *department_names).grid(column=1,row=4)
        
        tk.Button(self.root, text="Create Account", command=lambda: self.try_create_account(var_name1.get(), var_name2.get(), var_password.get(), var_account_type.get(), var_department_name.get())).grid(column=1, row=5)
        tk.Button(self.root, text="Cancel", command=self.admin_gui).grid(column=0, row=5)

    def admin_gui(self):
        self.create_root()
        # button to open account creation GUI
        self.root.geometry('300x200')
        self.root.title("ADMIN")
        new_acc_button = tk.Button(self.root, text="New Account", font=('Courier New', 15), command=self.new_account_gui)
        new_acc_button.grid(row=1,column=0, sticky="w")
        tk.Label(self.root, text="", width=10).grid(row=0, column=0, columnspan=3)
        tk.Button(self.root, text="New Department", font=('Courier New', 15), command=self.new_department_gui).grid(row=2,column=0, sticky="w")
        tk.Label(self.root, text="", width=10).grid(row=3, column=0, columnspan=3)
        tk.Label(self.root, text="", width=10).grid(row=4, column=0, columnspan=3)
        tk.Label(self.root, text="", width=10).grid(row=5, column=0, columnspan=3)
        tk.Label(self.root, text="", width=10).grid(row=6, column=0, columnspan=3)
        tk.Label(self.root, text="", width=10).grid(row=7, column=0, columnspan=3)
        logout_button = tk.Button(self.root, text="Log out", font=('Courier New', 15, "bold"), fg="red", command=self.logout)
        logout_button.grid(row=7, column=1, sticky="we")


    def treasurer_gui(self):
        self.create_root()
        tk.Label(self.root, text=str(self.account.department.balance)+"$").grid(column=2, row=1)
        tk.Button(self.root, text="Deposit", command=lambda: self.money_gui(0)).grid(column=1, row=0)
        tk.Button(self.root, text="Withdraw", command=lambda: self.money_gui(1)).grid(column=1, row=1)
        tk.Button(self.root, text="Transfer", command=lambda: self.money_gui(2)).grid(column=1, row=2)
        tk.Button(self.root, text="Log Out", command=self.logout).grid(column=2, row=0)
        
    def login(self, account : Account):
        self.account = account
        if account.is_admin():
            self.admin_gui()
        elif account.is_treasurer():
            self.treasurer_gui()
        elif account.is_officer():
            self.officer_gui()
        else:
            print("Account error!")

    def try_login(self, var, password):
        acc_name = var.get()
        account = self.sys.find_account(acc_name)
        if account is None or account.password != password:
            tk.Label(self.root, text="Anmeldung fehlgeschlagen!\nVersuche es erneut.", fg="red").grid(row=3,column=0, columnspan=3)
            return
        self.login(account)
    def login_gui(self):
        self.create_root()
        self.root.geometry('300x200')
        self.root.title("LOGIN")
        
        login_names = [acc.name for acc in self.sys.accounts]
        selected = tk.StringVar()

        username_menu = tk.OptionMenu(self.root, selected, *login_names)
        username_menu.grid(row=2, column=1, sticky="ew")
        self.root.columnconfigure(1, minsize=120)

        username_menu.configure(width=17)

        tk.Label(self.root, text="VEREINSKASSEN SYSTEM", font=('Courier New', 15, "bold"), justify="left",).grid(row=0, column=0, columnspan=2)
        tk.Label(self.root, text="", width=10).grid(row=1, column=0, columnspan=3)
        tk.Label(self.root, text="user:", font=('Courier New', 15), justify="left").grid(row=2,column=0)
        tk.Label(self.root, text="password:", font=('Courier New', 15), justify="left").grid(row=3, column=0)
        tk.Label(self.root, text="", width=10).grid(row=4, column=0, columnspan=3)
        
        password_var = tk.StringVar()
        password_entry = tk.Entry(self.root, show="*", textvariable=password_var , bg="black", fg="white")
        password_entry.grid(row=3,column=1)
        x = lambda: self.try_login(selected, password_var.get())
        password_entry.bind("<Return>", lambda event: self.try_login(selected, password_var.get()))
        login_button = tk.Button(self.root, text="login", font=('Courier New', 15, "bold"), justify="left", command=x)
        login_button.grid(row=5,column=0, columnspan=2)


if __name__ == "__main__":
    gui = SystemGUI()
    gui.start()