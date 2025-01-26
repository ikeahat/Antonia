__author__ = '8568922, Wolff'

import Tkinker

def account_perm_string(number):
    return ["Treasurer", "Finance Officer", "Admin"][number]

class Account:
    def __init__(self, name, password, account_type: int, department=None):
        self.name = name
        self.password = password
        self.account_type = account_type
        self.department = department
    
    def __str__(self):
        s = f"First name: {self.name[0]}\nLast name: {self.name[1]}\nAccount type: {account_perm_string(self.account_type)}"
        if self.department is not None:
            s += f"\nDepartment: {str(self.department)}"
        return s

class Department:
    def __init__(self, name, balance: int):
        self.name = name
        self.balace = balance
