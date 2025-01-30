import tkinter as tk
import tkinter.ttk as ttk
from vereinskasse import *


class SystemGUI:
    def __init__(self):
        self.sys = System("title", [], [])
        self.root = None

        admin_account = Account(("f", "l"), "abc", "admin")
        self.sys = System("title", [admin_account], [])
    def create_root(self):
        if self.root:
            self.root.destroy()
        self.root = tk.Tk()
    def clear(self):
        """Clear all widgets from tk screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
    def start(self):
        self.login_gui()
        self.root.mainloop()
    def new_account_gui(self):
        self.create_root()
        # all tk vars
        var_name1 = tk.StringVar()
        var_name2 = tk.StringVar()
        var_password = tk.StringVar()
        var_account_type = tk.StringVar()
        # tk entry fields
        tk.Entry(self.root, textvariable=var_name1).grid(column=1, row=0)
        tk.Entry(self.root, textvariable=var_name2).grid(column=1, row=1)
        tk.Entry(self.root, textvariable=var_password, show="*", bg="black", fg="white").grid(column=1, row=2)
        account_types = ["admin", "treasurer", "officer"]
        tk.OptionMenu(self.root, var_account_type, *account_types).grid(column=1,row=3)
        # TODO Auswahl für Departments (sofern treasurer account)
        # TODO Button to actually create account and return to previous window etc.
        for i in range(4):
            tk.Label(self.root, text=(["Vorname", "Nachname", "Passwort", "Accounttyp"][i])).grid(column=0, row=i)

    def admin_gui(self):
        self.create_root()
        # button to open account creation GUI
        new_acc_button = tk.Button(self.root, text="Neues Nutzerkonto", command=self.new_account_gui)
        new_acc_button.grid(row=0,column=0,columnspan=2)

    def login(self, account : Account):
        self.account = account
        self.admin_gui()

    def try_login(self, var, password):
        acc_name = var.get()
        account = self.sys.find_account(acc_name)
        if account is None or account.password != password:
            tk.Label(self.root, text="Anmeldung fehlgeschlagen!\nVersuche es erneut.", fg="red").grid(row=3,column=0, columnspan=3)
            return
        self.login(account)
    def login_gui(self):
        self.create_root()

        login_names = [acc.name for acc in self.sys.accounts]
        selected = tk.StringVar()
        username_menu = tk.OptionMenu(self.root, selected, *login_names)
        username_menu.grid(row=0, column=1)  
        
        tk.Label(self.root, text="user:").grid(row=0,column=0)
        tk.Label(self.root, text="password:").grid(row=1, column=0)
        
        password_var = tk.StringVar()
        password_entry = tk.Entry(self.root, show="*", textvariable=password_var , bg="black", fg="white")
        password_entry.grid(row=1,column=1)
        x = lambda: self.try_login(selected, password_var.get())
        password_entry.bind("<Return>", lambda event: self.try_login(selected, password_var.get()))
        login_button = tk.Button(self.root, text="login", command=x)
        login_button.grid(row=2,column=0,columnspan=2)


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