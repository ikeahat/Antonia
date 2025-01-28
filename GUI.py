import tkinter as tk
import tkinter.ttk as ttk
from vereinskasse import *


class SystemGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.sys = System("title", [], [])
    def clear(self):
        """Clear all widgets from tk screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
    def start(self):
        self.root.mainloop()
    def login_gui(self):
        selected = tk.StringVar()
        login_names = [acc.name for acc in self.sys.accounts]
        username_menu = tk.OptionMenu(self.root, selected, *login_names)
        username_menu.grid(row=0,column=1)
        tk.Label(self.root, "Nutzer").grid(row=0,column=0)
        tk.Label(self.root, "Passwort").grid(row=1, column=0)
        password_entry = tk.Entry(self.root)
        password_entry.grid(row=1,column=1)


root = tk.Tk()

b0 = ttk.Button(root, text = "transfer", command = Department.transfer)
b0.pack()
b1 = ttk.Button(root, text = "Doch", command = hallo)
b1.pack()
b2 = tk.Button(root, text="Nein", command = root.destroy)
b2.pack()
root.mainloop()

'''gui = SystemGUI()
gui.sys.create_account(("admin", "admin"), "hiabc", 0)
gui.login_gui()
gui.start()'''