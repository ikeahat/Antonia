import tkinter as tk
import tkinter.ttk as ttk
from vereinskasse import *


class SystemGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.sys = System("title", [], [])

        admin_account = Account(("f", "l"), "abc", "admin")
        self.sys = System("title", [admin_account], [])
    def create_root(self):
        self.root = tk.Tk()
    def clear(self):
        """Clear all widgets from tk screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
    def start(self):
        self.login_gui()
        self.root.mainloop()
    def try_login(self, var, password) -> bool:
        acc_name = var.get()
        account = self.sys.find_account(acc_name)
        print(acc_name)
        print(password)
        print(account.password)
        if account is None or account.password != password:
            return False
        
        self.root.destroy()
        self.create_root()
        

    def login_gui(self):
        selected = tk.StringVar()
        login_names = [acc.name for acc in self.sys.accounts]
        username_menu = tk.OptionMenu(self.root, selected, *login_names)
        username_menu.grid(row=0,column=1)
        tk.Label(self.root, text="Nutzer").grid(row=0,column=0)
        tk.Label(self.root, text="Passwort").grid(row=1, column=0)
        password_var = tk.StringVar()
        password_entry = tk.Entry(self.root, show="*", textvariable=password_var , bg="black", fg="white")
        password_entry.grid(row=1,column=1)
        login_button = tk.Button(self.root, text="Anmelden", command=lambda: self.try_login(selected, password_var.get()))
        login_button.grid(row=0,column=2,rowspan=2)


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