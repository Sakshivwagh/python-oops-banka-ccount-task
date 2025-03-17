from datetime import datetime
import unittest

class BankAccount:
    total_accounts = 0  # Class variable to track total accounts
    all_accounts = []  # Class variable to maintain a log of all accounts

    def __init__(self, account_holder, initial_balance=0):
        if not account_holder:
            raise ValueError("Account holder name cannot be empty.")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        
        self.account_holder = account_holder
        self.balance = initial_balance
        self.transactions = []
        BankAccount.total_accounts += 1
        BankAccount.all_accounts.append(self)
        self.transactions.append(f"Account created with balance ₹{initial_balance}")
        print(f"New account created for {self.account_holder}.")

    def deposit(self, amount):
        if not self.validate_amount(amount):
            return "Invalid deposit amount."
        self.balance += amount
        self.transactions.append(f"Deposited ₹{amount}. New balance: ₹{self.balance}")
        return f"Deposited ₹{amount}. Balance: ₹{self.balance}"

    def withdraw(self, amount):
        if not self.validate_amount(amount):
            return "Invalid withdrawal amount."
        if self.balance - (amount + 10) < 0:  # Transaction fee ₹10
            return "Insufficient funds."
        self.balance -= (amount + 10)
        self.transactions.append(f"Withdrew ₹{amount} (₹10 fee applied). New balance: ₹{self.balance}")
        return f"Withdrew ₹{amount}. Balance: ₹{self.balance}"

    def transfer(self, recipient, amount):
        if not isinstance(recipient, BankAccount):
            return "Invalid recipient."
        if not self.validate_amount(amount):
            return "Invalid transfer amount."
        if self.balance - amount < 0:
            return "Insufficient funds."
        
        self.balance -= amount
        recipient.balance += amount
        self.transactions.append(f"Transferred ₹{amount} to {recipient.account_holder}. New balance: ₹{self.balance}")
        recipient.transactions.append(f"Received ₹{amount} from {self.account_holder}. New balance: ₹{recipient.balance}")
        return f"Transferred ₹{amount} to {recipient.account_holder}."

    def check_balance(self):
        return f"Balance: ₹{self.balance}"

    def get_transaction_history(self):
        return "\n".join(self.transactions)

    @classmethod
    def total_bank_accounts(cls):
        return f"Total bank accounts: {cls.total_accounts}"

    @staticmethod
    def validate_amount(amount):
        return isinstance(amount, (int, float)) and 0 < amount <= 50000

# Subclasses for Savings and Current Accounts
class SavingsAccount(BankAccount):
    interest_rate = 0.05  # 5% annual interest
    min_balance = 1000

    def __init__(self, account_holder, initial_balance=1000):
        if initial_balance < self.min_balance:
            raise ValueError(f"Minimum balance for Savings Account is ₹{self.min_balance}")
        super().__init__(account_holder, initial_balance)

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        self.transactions.append(f"Interest of ₹{interest} applied. New balance: ₹{self.balance}")
        return f"Interest of ₹{interest} applied. New balance: ₹{self.balance}"

class CurrentAccount(BankAccount):
    def __init__(self, account_holder, initial_balance=0):
        super().__init__(account_holder, initial_balance)

# Unit Tests
class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.acc1 = BankAccount("Alice", 5000)
        self.acc2 = BankAccount("Bob", 3000)

    def test_deposit(self):
        self.assertEqual(self.acc1.deposit(2000), "Deposited ₹2000. Balance: ₹7000")
        self.assertEqual(self.acc1.deposit(60000), "Invalid deposit amount.")
    
    def test_withdraw(self):
        self.assertEqual(self.acc1.withdraw(1000), "Withdrew ₹1000. Balance: ₹3990")
        self.assertEqual(self.acc1.withdraw(50000), "Invalid withdrawal amount.")
    
    def test_transfer(self):
        self.assertEqual(self.acc1.transfer(self.acc2, 2000), "Transferred ₹2000 to Bob.")
        self.assertEqual(self.acc1.transfer(self.acc2, 60000), "Invalid transfer amount.")

if __name__ == "__main__":
    while True:
        print("\nBank Account Management System")
        print("1. Create Savings Account")
        print("2. Create Current Account")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Transfer Money")
        print("6. Check Balance")
        print("7. View Transaction History")
        print("8. Exit")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter account holder name: ")
            amount = float(input("Enter initial deposit: "))
            acc = SavingsAccount(name, amount)
        elif choice == "2":
            name = input("Enter account holder name: ")
            amount = float(input("Enter initial deposit: "))
            acc = CurrentAccount(name, amount)
        elif choice == "3":
            amount = float(input("Enter amount to deposit: "))
            print(acc.deposit(amount))
        elif choice == "4":
            amount = float(input("Enter amount to withdraw: "))
            print(acc.withdraw(amount))
        elif choice == "5":
            recipient_name = input("Enter recipient's name: ")
            amount = float(input("Enter amount to transfer: "))
            recipient = next((a for a in BankAccount.all_accounts if a.account_holder == recipient_name), None)
            if recipient:
                print(acc.transfer(recipient, amount))
            else:
                print("Recipient account not found.")
        elif choice == "6":
            print(acc.check_balance())
        elif choice == "7":
            print(acc.get_transaction_history())
        elif choice == "8":
            break
        else:
            print("Invalid choice. Try again.")
