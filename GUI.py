import tkinter as tk
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
        print(login_names)
        om = tk.OptionMenu(self.root, login_names, *login_names)
        om.pack()


gui = SystemGUI()
gui.sys.create_account(("admin", "admin"), "hiabc", 0)
gui.login_gui()
gui.start()