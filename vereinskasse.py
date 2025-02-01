"""
Module for backend of Virtual Club Cash Register Program.
"""
# TODO author

# Imports.
import tkinter as tk
import csv
import os

from datetime import datetime


class Account:
    """
    Account class. Represents a single user account in the system.
    Consists of first and last name (tuple of str), password (str),
    account type (str) and department (Department)
    """
    def __init__(self, name, password, acc_type, department = None):
        """
        Init method of Account. Puts parameters into class attributes.
        """
        self.name = name
        self.password = password
        self.acc_type = acc_type
        self.department = department


    def is_admin(self) -> bool:
        """
        Returns whether this account is an admin.
        """
        return self.acc_type == "admin"


    def is_treasurer(self) -> bool:
        """
        Returns whether this account is a treasurer.
        """
        return self.acc_type == "treasurer"


    def is_officer(self) -> bool:
        """
        Returns whether this account is a finance officer.
        """
        return self.acc_type == "officer"


    def get_department_name(self) -> str:
        """
        Returns the name of this users department if the user is a
        treasurer (else it returns "").
        """
        if self.department is None:
            return ""
        return self.department.name


class Department:
    """
    A class representing a single club department in the system.
    Consists of the department name, current balance as well as
    a history of all transactions of this department.
    """
    def __init__(self, name, balance: float):
        """
        Basic init function. Takes a name and balance as a parameter and
        creates an empty list for transactions
        """
        self.transactions = []
        self.name = name
        self.balance = balance
    def log_transaction(self, amount : float, text : str):
        """
        Enters a transaction of the given parameters into self.transactions.
        Also adds the current datetime into the text of the transaction.
        """
        self.transactions.append(Transaction(amount, f"{text} at {str(datetime.now())}"))


    def can_pay(self, amount : float) -> bool:
        """
        Returns a bool value of whether the department can afford to pay
        the amount specified in the parameter.
        """
        return self.balance - amount >= 0


    def withdrawal(self, amount: float):
        """
        Tries to withdraw (remove) an amount of money specified in the
        parameter. If the departments balance is not sufficient, return False.
        On success, return True.
        """
        if not self.can_pay(amount):
            return False  # Check if balance is sufficient.
        self.balance = self.balance - amount  # Reduce balance.
        self.log_transaction(-amount, "Withdrawal")  # Log withdrawal.
        return True


    def deposit(self, amount: float):
        """
        Add money of amount given in parameter to the account.
        """
        self.balance = self.balance + amount  # Add money.
        self.log_transaction(amount, "Deposit")  # Log in history.


    def transfer(self, amount: float, recipient):
        """
        Tries to transfer money to another club department. Returns
        whether the transaction is successful (which is the case if this
        department has enough money (see can_pay)) as bool.
        """
        if not self.can_pay(amount):
            return False  # Check if balance is sufficient.
        self.balance = self.balance - amount  # Reduce balance.
        recipient.balance = recipient.balance + amount  # Add balance to recipient
        self.log_transaction(-amount, "Transfer to "+recipient.name)  # Log transaction history.
        recipient.log_transaction(amount, "Transfer from "+self.name)  # Log in recipient history.
        return True  # Return True.


class Transaction:
    """
    A class representing a single department transaction.
    """
    def __init__(self, amount, text):
        """
        Init function for Transaction. This class has 2 attributes, text
        and amount.
        """
        self.amount = amount
        self.text = text


class System:
    """
    System class. This is where all lists of accounts, departments etc. come
    together and are managed.
    """
    def __init__(self):
        """
        Basic init function which creates empty lists for accounts and
        departments.
        """
        self.accounts = []
        self.departments = []

    def get_total_balance(self):
        """
        Returns the total combined balance of all club departments.
        """
        total = 0
        for department in self.departments:
            total += department.balance
        return total

    def load_if_exists(self):
        """
        Loads accounts and departments data if "data" folder exists.
        (using self.load())
        """
        if os.path.isdir("data"):
            self.load()  # Load data and append nothing else if data already exists.
        else:
            # If data folder doesn't exist, create default admin account.
            self.create_account(("admin", "admin"), "admin", "admin", None)
            self.save_all()  # Save new state.


    def load(self):
        """
        Load files of accounts, departments and transaction histories
        and put into respective class attributes.
        """
        # Load departments.
        with open("data/departments.csv", newline = "") as file:
            for row in csv.reader(file):
                department = Department(row[0], float(row[1]))
                self.departments.append(department)
        # Load accounts.
        with open("data/accounts.csv", newline = "") as file:
            for row in csv.reader(file):
                account = Account((row[0], row[1]), row[2], row[3], self.find_department(row[4]))
                self.accounts.append(account)
        # Load transaction histories of departments.
        # Loop through each file in data/transactions.
        for filename in os.listdir("data/transactions/"):
            d = self.find_department(filename.removesuffix(".csv"))  # Get department instance.
            if d is None:  # In case there is data of a non existent department.
                continue  # Skip this element.
            # Read csv file of this departments transaction history.
            with open("data/transactions/"+filename, newline = "") as file:
                for row in csv.reader(file):  # csv is structured amount,text
                    d.transactions.append(Transaction(float(row[0]), row[1]))


    def create_account(self, name, password, acc_type, department = None):
        """
        Creates a new account of parameters and registers into list.
        """
        a = Account(name, password, acc_type, department)
        self.accounts.append(a)
    def create_department(self, name, balance: float):
        """
        Creates a new department of parameters and registers into list.
        """
        a = Department(name, balance)
        self.departments.append(a)


    def find_account(self, name) -> Account:
        """
        Search for account in self.accounts which has a name which equals the
        parameter. Return Account if there is one, else return None.
        """
        for acc in self.accounts:
            if str(acc.name) == name:
                return acc


    def find_department(self, name) -> Department:
        """
        Search for department in self.departments which has a name which
        equals the parameter. Return Department if there is one,
        else return None.
        """
        for dep in self.departments:
            if dep.name == name:
                return dep


    def create_directories(self):
        """
        Check for file path data/transactions and create if doesnt exist.
        data/ contains accounts and departments files
        data/transactions/ contains transaction histories
        """
        path = "data/transactions"  # Directory path.
        if not (os.path.exists(path) and os.path.isdir(path)):
            # Make dirs if they do not already exist.
            os.makedirs("data/transactions")


    def save_accounts(self):
        """
        Saves all accounts data in accounts.csv.
        """
        # Create list of list of accounts data.
        # To be interpreted as a list of rows for the csv file.
        # One "row" is a list of elements containing an element for each column.
        data = [[acc.name[0],
                 acc.name[1],
                 acc.password,
                 acc.acc_type,
                 acc.get_department_name()] for acc in self.accounts]
        with open("data/accounts.csv", "w", newline = "") as file:
            csv.writer(file).writerows(data)  # Write data.


    def save_departments(self):
        """
        Save all departments data (name and current balance)
        in departments.csv.
        """
        data = [[dpt.name, dpt.balance] for dpt in self.departments]  # Create list of rows.
        with open("data/departments.csv", "w", newline = "") as file:
            csv.writer(file).writerows(data)  # Write data.


    def save_departments_history(self):
        """
        Save transaction histories of all departments. Each department gets
        one .csv file in data/transactions named after the department name
        (+".csv").
        """
        for department in self.departments:  # Loop through each department.
            data = [[t.amount, t.text] for t in department.transactions]  # Generate rows.
            with open("data/transactions/" + department.name + ".csv", "w", newline = "") as file:
                csv.writer(file).writerows(data)  # Write data.


    def save_all(self):
        """
        Calls all data saving functions after calling the directory check function.
        """
        self.create_directories()  # Create dirs if not already existant.
        # Save all data.
        self.save_accounts()
        self.save_departments()
        self.save_departments_history()
