# TODO author

import tkinter as tk

from datetime import datetime
def account_perm_string(number):
    return ["Treasurer", "Finance Officer", "Admin"][number]

class Account:
    def __init__(self, name, password, type: int, department=None):
        self.name = name
        self.password = password
        self.type = type
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
        type = "withdrawal"
        text = "has withdrawn"
        amount = input("amount:")
        if self.can_pay() == True:
            self.balance = self.balance - amount
        a = Transaction(self, amount, type, text)
        self.transactions.append(a)
    def deposit(self, amount: int):
        type = "deposit"
        text = "has deposited"
        amount = input("amount:")
        self.balance = self.balance + amount
        a = Transaction(self, amount, type, text)
        self.transactions.append(a)
    def transfer(self, amount: int, recipient: Department):
        display_departments()  # Choose recipient
        type = "transfer"
        text = "has transfered"
        amount = input("amount:")
        if self.can_pay() == True:
            self.balance = self.balance - amount
            recipient.balance = recipient.balance + amount
        a = Transaction(self, amount, type, text)
        self.transactions.append(a)

transactions = []

class Transaction:
    def __init__(self, amount, type, text, sender_name):
        self.sender_name = sender_name
        self.type = type
        self.amount = amount
        self.text = text
        self.time = str(datetime.now())

class System:
    def __init__(self, title, accounts: list, departments: list):
        self.title = title
        self.accounts = []
        self.departments = []
    def create_account(self, name, password, type: int, department = None):
        a = Account(name, password, type, department)
        self.accounts.append(a)
    def find_account(self, name):
        for acc in self.accounts:
            if acc.name == name:
                return acc
    def add_to_transaction_history():
        transaction_filename = f"transaction history: {Department}.txt"
        with open(transaction_filename, "a") as f:
            for transaction in transactions:
                f.write(transaction.time)
                if transaction.type == "withdrawal" or "deposit":
                    f.write({transaction.sender_name} + {transaction.text} + {transaction.amount})
                elif transaction.type == "transfer":
                    f.write(f"{transaction.sender_name} + {transaction.text} + {transaction.amount} to {transaction.recipient}")
    def save_current_balance(self):
        for department in self.departments:
            balance_filename = "balance"
            with open(balance_filename, "a") as f:
                f.write(department.balance)