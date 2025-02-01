# TODO author

import tkinter as tk
import csv
import os

from datetime import datetime
def account_perm_string(number):
    return ["Treasurer", "Finance Officer", "Admin"][number]

class Account:
    def __init__(self, name, password, acc_type: int, department=None):
        self.name = name
        self.password = password
        self.acc_type = acc_type
        self.department = department
    
    def __str__(self):
        s = f"First name: {self.name[0]}\nLast name: {self.name[1]}\nAccount type: {account_perm_string(self.acc_type)}"
        if self.department is not None:
            s += f"\nDepartment: {str(self.department)}"
        return s
    def is_admin(self):
        return self.acc_type == "admin"
    def is_treasurer(self):
        return self.acc_type == "treasurer"
    def is_officer(self):
        return self.acc_type == "officer"
    def get_department_name(self):
        if self.department is None:
            return ""
        return self.department.name

class Department:
    def __init__(self, name, balance: int):
        self.transactions = []
        self.name = name
        self.balance = balance
    def log_transaction(self, amount : int, text : str):
        self.transactions.append(Transaction(amount, f"{text} at {str(datetime.now())}"))
    def can_pay(self, amount : float) -> bool:
        return self.balance - amount >= 0
    def withdrawal(self, amount: float):
        if not self.can_pay(amount):
            return False
        self.balance = self.balance - amount
        self.log_transaction(-amount, "Withdrawal")
        return True
    def deposit(self, amount: float):
        self.balance = self.balance + amount
        self.log_transaction(amount, "Deposit")
    def transfer(self, amount: float, recipient):
        if not self.can_pay(amount):
            return False
        self.balance = self.balance - amount
        recipient.balance = recipient.balance + amount
        self.log_transaction(-amount, "Transfer to "+recipient.name)
        recipient.log_transaction(amount, "Transfer from "+self.name)
        return True
class Transaction:
    def __init__(self, amount, text):
        self.amount = amount
        self.text = text
class System:
    def __init__(self):
        self.accounts = []
        self.departments = []
    def load_if_exists(self):
        if os.path.isdir("data"):
            self.load()
        else:
            self.create_account(("admin", "admin"), "admin", "admin", None)
            self.save_all()
    def load(self):
        # departments
        with open("data/departments.csv", newline="") as file:
            for row in csv.reader(file):
                department = Department(row[0], float(row[1]))
                self.departments.append(department)
        # accounts
        with open("data/accounts.csv", newline="") as file:
            for row in csv.reader(file):
                account = Account((row[0], row[1]), row[2], row[3], self.find_department(row[4]))
                self.accounts.append(account)
        # transaction histories
        for filename in os.listdir("data/transactions/"):
            d = self.find_department(filename.removesuffix(".csv"))
            print(filename.removesuffix(".csv"))
            if d is None:
                continue
            with open("data/transactions/"+filename, newline="") as file:
                for row in csv.reader(file):
                    d.transactions.append(Transaction(float(row[0]), row[1]))
    def create_account(self, name, password, type: int, department = None):
        a = Account(name, password, type, department)
        self.accounts.append(a)
    def create_department(self, name, balance: int):
        a = Department(name, balance)
        self.departments.append(a)
    def find_account(self, name) -> Account:
        for acc in self.accounts:
            if str(acc.name) == name:
                return acc
    def find_department(self, name) -> Department:
        for dep in self.departments:
            if dep.name == name:
                return dep
    def create_directories(self):
        path = "data/transactions"
        if not (os.path.exists(path) and os.path.isdir(path)):
            os.makedirs("data/transactions")
    def save_accounts(self):
        data = [[acc.name[0],
                 acc.name[1],
                 acc.password,
                 acc.acc_type,
                 acc.get_department_name()] for acc in self.accounts]
        with open("data/accounts.csv", "w", newline="") as file:
            csv.writer(file).writerows(data)
    def save_departments(self):
        data = [[dpt.name, dpt.balance] for dpt in self.departments]
        with open("data/departments.csv", "w", newline="") as file:
            csv.writer(file).writerows(data)
    def save_departments_history(self):
        for department in self.departments:
            data = [[t.amount, t.text] for t in department.transactions]
            with open("data/transactions/" + department.name + ".csv", "w", newline="") as file:
                csv.writer(file).writerows(data)
    def save_all(self):
        self.create_directories()
        self.save_accounts()
        self.save_departments()
        self.save_departments_history()
