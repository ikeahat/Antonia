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

departments = []

def display_departments():
    print("\nDepartments:")
    for idx, department in enumerate(departments):
        print(f"{idx}: {department['name']}")


class Department:
    def __init__(self, name, balance: int):
        self.name = name
        self.balance = balance
    def can_pay(self, balance, amount) -> bool:
        return self.balance - self.amount >= 0
    def withdrawal(self, amount: int):
        amount = input("amount:")
        if self.can_pay() == True:
            self.balance = self.balance - amount
    def deposit(self, amount: int):
        amount = input("amount:")
        self.balance = self.balance + amount
    def transfer(self, amount: int, recipient: Department):
        display_departments()  # Choose recipient
        amount = input("amount:")
        if self.can_pay() == True:
            self.balance = self.balance - amount
            recipient.balance = recipient.balance + amount