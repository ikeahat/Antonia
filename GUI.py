import tkinter as tk
import tkinter.ttk as ttk
from vereinskasse import *

class SystemGUI:
    def __init__(self):
        self.sys = System("title", [], [])
        self.root = None

        admin_account = Account(("first", "last"), "abc", "admin")
        self.sys = System("title", [admin_account], [])
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

    def transfer_gui(self):
        department_names = [d.name for d in self.sys.departments]
        self.create_root()
        selected = tk.StringVar()
        var_amount = tk.IntVar()
        tk.OptionMenu(self.root, selected, *department_names).grid(column=1, row=0)
        tk.Entry(self.root, intvariable=var_amount).grid(column=1, row=1)

    def deposit_gui(self):
        self.create_root()
        var_amount = tk.IntVar()
        tk.Entry(self.root, intvariable=var_amount).grid(column=1, row=1)

    def withdraw_gui(self):
        self.create_root()
        var_amount = tk.IntVar()
        tk.Entry(self.root, intvariable=var_amount).grid(column=1, row=1)

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
        new_transfer_button = tk.Button(self.root, text="transfer", command=self.transfer_gui)
        new_deposit_button = tk.Button(self.root, text="deposit", command=self.deposit_gui)
        new_withdraw_button = tk.Button(self.root, text="withdraw", command=self.withdraw_gui)
        
    def login(self, account : Account):
        self.account = account
        if account.is_admin():
            self.admin_gui()
        elif account.is_treasurer():
            self.treasurer_gui()
        #elif account.is_officer():
            #self.officer_gui()

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


'''b0 = ttk.Button(root, text = "transfer", command = Department.transfer)
b0.pack()
b1 = ttk.Button(root, text = "Doch", command = hallo)
b1.pack()
b2 = tk.Button(root, text="Nein", command = root.destroy)
b2.pack()'''

'''gui = SystemGUI()
gui.sys.create_account(("admin", "admin"), "hiabc", 0)
gui.login_gui()
gui.start()'''

if __name__ == "__main__":
    gui = SystemGUI()
    gui.start()