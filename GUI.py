"""
Virtual Club Cash Register Program GUI Module (frontend).
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from vereinskasse import *

class SystemGUI:
    """
    A class which manages the GUI in combination with the System.
    """
    def __init__(self):
        """
        Init function for SystemGUI. 
        Creates a system object and loads data if existant.
        """
        self.sys = System()
        self.root = None
        self.account = None
        self.sys.load_if_exists()


    def create_root(self):
        """
        Creates a new (centered) root window and destroys the previous one.
        """
        if self.root:
            self.root.destroy()
        self.root = tk.Tk()
        self.center_window()
    def center_window(self, width=400, height=300):
        """
        Root window is centerd on the screen.
        """
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    def start(self):
        """
        Start up the application. Calls the login_gui method and starts
        self.root.mainloop()
        """
        self.login_gui()  # Login GUI is called.
        self.root.mainloop()  # Mainloop is called.
    def logout(self):
        """
        Logs the user out and returns to the login GUI.
        """
        self.account = None  # Logged in account ist reset.
        self.login_gui()  # Login GUI is called
        self.sys.save_all()  # Save all data into file system on logout.


    def try_create_department(self, name):
        """
        Try to create a department of the parameter name.
        """
        if name == "":  # Check whether the entered name is empty.
            messagebox.showerror(text="Please enter a valid department name.")  # Error popup.
            return
        # Check whether department name is already used.
        if self.sys.find_department(name) is not None:
            messagebox.showerror(text="This department already exists.")  # Error popup.
            return
        self.sys.create_department(name, 0.0)  # Create department in system.
        self.admin_gui()  # Return to admin view.


    def new_department_gui(self):
        """
        Opens the GUI for creating a new department.
        """
        self.create_root()
        self.root.geometry("350x100")
        self.root.title("NEW DEPARTMENT")
        var_name = tk.StringVar()  # Tk var.
        # Place holders that keep the grid in shape.
        tk.Label(self.root, text="", width=10).grid(row=0, column=0, columnspan=3)
        tk.Label(self.root, text="", width=10).grid(row=1, column=0, columnspan=3)
        tk.Entry(self.root, textvariable=var_name).grid(column=1,row=1)  # Entry field for name.
        tk.Label(self.root, text="Department name:", font=('Courier New', 15)).grid(column=0,row=1)
        tk.Button(self.root, text="Create Department", font=('Courier New', 15), 
                  command=lambda: self.try_create_department(var_name.get())).grid(column=1, row=2)
        tk.Button(self.root, text="Cancel", fg="red", font=('Courier New', 15), 
                  command=self.admin_gui).grid(column=0,row=2)


    def try_create_account(self, name1, name2, password, acc_type, department_name):
        """
        Tries to create an account with the given parameters as data.
        """
        # Check whether something is left with no input.
        invalid = False
        for s in [name1, name2, password, acc_type]:  # All params as iterable list.
            if s == "":
                invalid = True
                break
        department = None
        # Check for department field if acctype is treasurer.
        if acc_type == "treasurer":
            if department_name == "":  # Check whether department name is selected.
                invalid = True
            else:
                department = self.sys.find_department(department_name)  # Get department object.
                if department is None:  # Check if selected department exists.
                    invalid = True
        if invalid:  # Output invalid input message.
            messagebox.showerror(text="Invalid input.")
            return
        if self.sys.find_account((name1, name2)) is not None:  # Check if account already exists.
            messagebox.showerror(text="Account already exists.")  # Error if it does exist.
            return
        self.sys.create_account((name1, name2), password, acc_type, department)  # Create account.
        self.admin_gui()  # Return to admin view


    def try_money_operation(self, arg, amount, target):
        """
        Try to commence a money operation. This may be a deposit, withdrawal,
        or transfer to another club account. The parameters are:
        arg - what kind of operation it is (0=deposit, 1=withdraw, 2=transfer)
        amount - the amount of money
        target - the target department in case of transfer (else may be None)
        """
        try:
            amount = float(amount)  # Check if string is float-able.
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
        """
        GUI for money operations. The arg param determines which operation
        the GUI currently handles (0=deposit, 1=withdraw, 2=transfer).
        """
        self.create_root()
        self.root.geometry("400x100")
        self.root.title(["Deposit Money", "Withdraw Money", "Transfer Money"][arg])
        
        var_amount = tk.StringVar()
        tk.Label(self.root, text="", width=10).grid(row=0, column=0, columnspan=3)
        tk.Label(self.root, font=('Courier New', 15), text="Amount:").grid(row=1,column=0)
        tk.Label(self.root, text="", width=10).grid(row=2, column=0, columnspan=3)
        tk.Entry(self.root, font=('Courier New', 15), textvariable=var_amount).grid(row=1,column=1)
        var_department = tk.StringVar()
        if arg == 2:
            department_names = [d.name for d in self.sys.departments]
            department_names.remove(self.account.department.name)  # remove own department
            department_names.append("")
            tk.OptionMenu(self.root, var_department, *department_names).grid(column=3, row=1)
        
        tk.Button(self.root, font=('Courier New', 15), text="Execute", command = lambda: self.try_money_operation(arg, var_amount.get(), var_department.get())).grid(row=3,column=1)
        tk.Button(self.root, font=('Courier New', 15), text="Cancel", fg="red", command=self.treasurer_gui).grid(column=0, row=3)


    def new_account_gui(self):
        """
        Creates the GUI for entering the data of a new account
        (account creation GUI).
        """
        self.create_root()
        self.root.geometry("350x250")
        self.root.title("CREATE ACCOUNT")
        
        # all tk vars
        var_name1 = tk.StringVar()
        var_name2 = tk.StringVar()
        var_password = tk.StringVar()
        var_account_type = tk.StringVar()
        var_department_name = tk.StringVar()
        # tk entry fields

        tk.Label(self.root, text="", width=10).grid(row=2, column=0, columnspan=3)
        tk.Entry(self.root, textvariable=var_name1).grid(column=1, row=3)
        tk.Entry(self.root, textvariable=var_name2).grid(column=1, row=4)
        tk.Entry(self.root, textvariable=var_password, show="*").grid(column=1, row=5)

        account_types = ["admin", "treasurer", "officer"]
        department_names = [d.name for d in self.sys.departments]
        department_names.append("")

        var_account_type.set(account_types[0])
        tk.OptionMenu(self.root, var_account_type, *account_types).grid(column=1,row=6, sticky="ew")
        self.root.columnconfigure(1, minsize=120)
        for i in range(5):
            tk.Label(self.root, font=('Courier New', 15), text=(["First Name", "Last Name", "Password", "Account Type", "Department\n(for treasurers)"][i])).grid(column=0, row=i+3)
        tk.OptionMenu(self.root, var_department_name, *department_names).grid(column=1,row=7, sticky="ew")
        
        tk.Button(self.root, text="Create Account", font=('Courier New', 15), command=lambda: self.try_create_account(var_name1.get(), var_name2.get(), var_password.get(), var_account_type.get(), var_department_name.get())).grid(column=1, row=8)
        tk.Button(self.root, text="Cancel", font=('Courier New', 15), fg="red", command=self.admin_gui).grid(column=0, row=8)


    def admin_gui(self):
        """
        Opens the Admin GUI, containing the buttons leading to the admin
        menus (account and department creation) as well as a log out button.
        """
        self.create_root()
        # button to open account creation GUI
        self.root.geometry('300x200')
        self.root.title("ADMIN")

        # Create new account button.
        new_acc_button = tk.Button(self.root, text="New Account", font=('Courier New', 15), command=self.new_account_gui)
        new_acc_button.grid(row=1,column=0, sticky="w")
        tk.Label(self.root, text="", width=10).grid(row=0, column=0, columnspan=3)
        # New department creation button.
        tk.Button(self.root, text="New Department", font=('Courier New', 15), command=self.new_department_gui).grid(row=2,column=0, sticky="w")
        # Empty space. Because grid wont respect my rows and columns.
        tk.Label(self.root, text="", width=10).grid(row=3, column=0, columnspan=3)
        tk.Label(self.root, text="", width=10).grid(row=4, column=0, columnspan=3)
        tk.Label(self.root, text="", width=10).grid(row=5, column=0, columnspan=3)
        tk.Label(self.root, text="", width=10).grid(row=6, column=0, columnspan=3)
        tk.Label(self.root, text="", width=10).grid(row=7, column=0, columnspan=3)
        # Logout button.
        logout_button = tk.Button(self.root, text="Log out", font=('Courier New', 15, "bold"), fg="red", command=self.logout)
        logout_button.grid(row=7, column=1, sticky="we")

    def officer_gui(self):
        """
        Creates the GUI for a finance officer account.
        """
        self.create_root()
        tk.Button(self.root, text="Log Out", command=self.logout).grid(column=1, row=0)
        # Department wise summary.
        tk.Button(self.root, text="Summary", command=self.summary_gui).grid(column=0, row=0)
        department_names = [d.name for d in self.sys.departments]
        # Dep list cant be empty.
        department_names.append("")
        var_department_name = tk.StringVar()
        tk.OptionMenu(self.root, var_department_name, *department_names).grid(column=0,row=1)
        tk.Button(self.root, text="View Department", command=lambda: self.try_department_history_gui(var_department_name.get())).grid(column=1, row=1)

    def treasurer_gui(self):
        """
        Opens the Treasurer GUI containing the options of a treasurer account.
        Contains buttons for all 3 money operations of the accounts department
        and a log-out button.
        """
        self.create_root()
        self.root.title("TRANSACTIONS")
        self.root.geometry("300x180")
        tk.Label(self.root, text = "", width = 10).grid(row = 0, column = 0, columnspan = 3)
        tk.Label(self.root, font = ('Courier New', 15), text=f"${self.account.department.balance:.2f}").grid(column = 2, row = 5)  
        # IYKYK :D ":.2f" wurde wieder eingeschleußt.
        tk.Button(self.root, text = "Deposit", font=('Courier New', 15), command = lambda: self.money_gui(0)).grid(column = 0, row = 1)
        tk.Button(self.root, text = "Withdraw", font=('Courier New', 15), command = lambda: self.money_gui(1)).grid(column = 0, row = 2)
        tk.Button(self.root, text = "Transfer", font=('Courier New', 15), command = lambda: self.money_gui(2)).grid(column = 0, row = 3)
        tk.Button(self.root, text = "Log Out", font=('Courier New', 15), fg="red", command=self.logout).grid(column = 0, row = 5)
        tk.Label(self.root, text = "", width = 10).grid(row = 4, column = 0, columnspan = 3)


    def summary_gui(self):
        """
        Opens a GUI which lists all departments along with their current 
        balance.
        """
        self.create_root()
        tk.Button(self.root, text="Return", fg="red", command=self.officer_gui).grid(column=1,row=0)
        tk.Label(self.root, text="Summary").grid(column=0,row=0)
        tk.Label(self.root, text="Total").grid(column=0,row=1)
        tk.Label(self.root, text=f"${self.sys.get_total_balance():.2f}").grid(column=1,row=1)
        for i in range(len(self.sys.departments)):
            d : Department = self.sys.departments[i]
            for j in range(2):
                tk.Label(self.root, text=(d.name, d.balance)[j]).grid(column=j, row=i+2)


    def try_department_history_gui(self, department_name):
        """
        Tries to show the transaction history of a selected department, if
        one is selected.
        """
        department = self.sys.find_department(department_name)
        # Error for bad request.
        if department is None:
            messagebox.showerror(message="Invalid target department.")
            return
        self.create_root()
        # Create summary for selected department.
        tk.Label(self.root, text=f"Summary of {department.name}").grid(column=0, row=0)
        tk.Button(self.root, text="Return", fg="red", command=self.officer_gui).grid(column=1, row=0)
        for i in range(len(department.transactions)):
            t : Transaction = department.transactions[i]
            prefix = ""
            if t.amount > 0:
                prefix = "+"
            for j in range(2):
                tk.Label(self.root, text=(prefix + str(t.amount), t.text)[j]).grid(column=j, row=i+1)


    def officer_gui(self):
        '''
        The gui that has all the functions for the finance officer.
        '''
        self.create_root()
        # Starts buttons.
        tk.Button(self.root, text="Log Out", command=self.logout).grid(column=1, row=0)
        tk.Button(self.root, text="Summary", command=self.summary_gui).grid(column=0, row=0)
        # Department list.
        department_names = [d.name for d in self.sys.departments]
        # In case there are no departments.
        department_names.append("")
        var_department_name = tk.StringVar()
        tk.OptionMenu(self.root, var_department_name, *department_names).grid(column=0,row=1)
        tk.Button(self.root, text="View Department", command=lambda: self.try_department_history_gui(var_department_name.get())).grid(column=1, row=1)


    def login(self, account : Account):
        """
        Logs in as the account specified in the account parameter.
        Calls the corresponting GUI function.
        """

        # Checks account type and starts whatever gui is the correct one.
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
        """
        Tries to login using the user name and password currently entered
        in the login GUI.
        """
        acc_name = var.get()
        account = self.sys.find_account(acc_name)
        # Outputs error for the case that the pass does not match the name.
        if account is None or account.password != password:
            messagebox.showerror(message="Login failed!\nUsername or password is wrong.")
            # Also pranking user becuase they can not input wrong usernames since its a drop down.
            return
        self.login(account)
    

    def login_gui(self):
        '''
        login_gui(self) function initializes the first window that pops up, when the program is being started. 
        '''
        self.create_root()
        self.root.geometry('300x200')  # Size.
        self.root.title("LOGIN")  # Title.
        
        login_names = [acc.name for acc in self.sys.accounts]  
        # Collects all account names in a list, for the Drop-down menu.
        selected = tk.StringVar()

        username_menu = tk.OptionMenu(self.root, selected, *login_names) 
        # Login usernames drop down menu. You may wonder why. Simply because we can.
        username_menu.grid(row=2, column=1, sticky="ew")  # Starts the grid.
        self.root.columnconfigure(1, minsize=120)

        username_menu.configure(width=17)  
        # This is the width of the drop down menu bar so it's consistent 
        # with the password input bar.
        
        # All the text.
        tk.Label(self.root, text="VIRTUAL CLUB\nCASH REGISTER PROGRAM", font=('Courier New', 15, "bold"), justify="left",).grid(row=0, column=0, columnspan=2)
        tk.Label(self.root, text="", width=10).grid(row=1, column=0, columnspan=3)
        tk.Label(self.root, text="user:", font=('Courier New', 15), justify="left").grid(row=2,column=0)
        tk.Label(self.root, text="password:", font=('Courier New', 15), justify="left").grid(row=3, column=0)
        tk.Label(self.root, text="", width=10).grid(row=4, column=0, columnspan=3)
        
        password_var = tk.StringVar()
        # Very professional password entry with asterisks. This makes so that the users get the 
        # impression, that we value cyber security. In reality, no password hashing is taking 
        # place >:) Muahahahahahah.
        password_entry = tk.Entry(self.root, show="*", textvariable=password_var)
        password_entry.grid(row=3,column=1)
        # Return key bound to do what clicking "login" does.
        password_entry.bind("<Return>", lambda event: self.try_login(selected, password_var.get()))
        tk.Button(self.root, text="login", font=('Courier New', 15, "bold"), justify="left", command=lambda: self.try_login(selected, password_var.get())).grid(row=5,column=0, columnspan=2)


if __name__ == "__main__":
    gui = SystemGUI()
    gui.start()