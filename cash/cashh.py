from datetime import datetime

class User:
    def __init__(self, name, phone_number, balance=0):
        self.name = name
        self.phone_number = phone_number
        self.balance = balance

    def deposit(self, amount, cash_system):
        self.balance += amount
        print(f"{self.name} has deposited {amount}. New balance is {self.balance}.")
        # Record the transaction
        transaction = Transaction(self, None, amount, "Deposit")
        cash_system.record_transaction(transaction)

    def withdraw(self, amount, cash_system):
        if amount > self.balance:
            print("Insufficient balance!")
        else:
            self.balance -= amount
            print(f"{self.name} has withdrawn {amount}. New balance is {self.balance}.")
            # Record the transaction
            transaction = Transaction(self, None, amount, "Withdrawal")
            cash_system.record_transaction(transaction)

    def send_money(self, recipient, amount, cash_system):
        if amount > self.balance:
            print("Insufficient balance!")
        else:
            self.balance -= amount
            recipient.balance += amount
            print(f"{self.name} sent {amount} to {recipient.name}. New balance is {self.balance}. {recipient.name}'s new balance is {recipient.balance}")
            # Record the transaction
            transaction = Transaction(self, recipient, amount, "Transfer")
            cash_system.record_transaction(transaction)

    def pay_bill(self, bill_name, amount, cash_system):
        if amount > self.balance:
            print("Insufficient balance to pay the bill!")
        else:
            self.balance -= amount
            print(f"{self.name} paid {amount} for {bill_name}. New balance is {self.balance}.")
            # Record the transaction
            transaction = Transaction(self, None, amount, f"Bill Payment ({bill_name})")
            cash_system.record_transaction(transaction)

    def buy_airtime(self, amount, cash_system):
        if amount > self.balance:
            print("Insufficient balance to buy airtime!")
        else:
            self.balance -= amount
            print(f"{self.name} bought {amount} worth of airtime. New balance is {self.balance}.")
            # Record the transaction
            transaction = Transaction(self, None, amount, "Airtime Purchase")
            cash_system.record_transaction(transaction)

class Transaction:
    def __init__(self, sender, recipient, amount, transaction_type):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.transaction_type = transaction_type
        self.date = datetime.now()

    def __repr__(self):
        recipient_name = self.recipient.name if self.recipient else "N/A"
        return f"[{self.date}] {self.transaction_type}: {self.sender.name} -> {recipient_name} | Amount: {self.amount}"

class eT3CashSystem:
    def __init__(self):
        self.users = {}
        self.transactions = []

    def add_user(self, user):
        if user.phone_number in self.users:
            print(f"User with phone number {user.phone_number} already exists.")
        else:
            self.users[user.phone_number] = user
            print(f"User {user.name} added to the system.")

    def get_user_by_phone(self, phone_number):
        return self.users.get(phone_number)

    def record_transaction(self, transaction):
        self.transactions.append(transaction)
        print(f"Transaction recorded: {transaction}")

    def get_transaction_history(self):
        for transaction in self.transactions:
            print(transaction)

    def perform_deposit(self, phone_number, amount):
        user = self.get_user_by_phone(phone_number)
        if user:
            user.deposit(amount, self)
        else:
            print("User not found.")

    def perform_withdrawal(self, phone_number, amount):
        user = self.get_user_by_phone(phone_number)
        if user:
            user.withdraw(amount, self)
        else:
            print("User not found.")

    def perform_transfer(self, sender_phone, recipient_phone, amount):
        sender = self.get_user_by_phone(sender_phone)
        recipient = self.get_user_by_phone(recipient_phone)
        if sender and recipient:
            sender.send_money(recipient, amount, self)
        else:
            print("One or both users not found.")

    def perform_bill_payment(self, phone_number, bill_name, amount):
        user = self.get_user_by_phone(phone_number)
        if user:
            user.pay_bill(bill_name, amount, self)
        else:
            print("User not found.")

    def perform_airtime_purchase(self, phone_number, amount):
        user = self.get_user_by_phone(phone_number)
        if user:
            user.buy_airtime(amount, self)
        else:
            print("User not found.")

# Example usage
eT3Cash = eT3CashSystem()

# Add users
user1 = User("Youseif Essam", "01003793415", balance=100)
user2 = User("Mohammed Fahmy", "01110989460", balance=20)

eT3Cash.add_user(user1)
eT3Cash.add_user(user2)

# Perform transactions
eT3Cash.perform_transfer("01003793415", "01110989460", 20)
eT3Cash.perform_deposit("01003793415", 50)
eT3Cash.perform_withdrawal("01110989460", 10)
eT3Cash.perform_bill_payment("01003793415", "Electricity", 30)
eT3Cash.perform_airtime_purchase("01110989460", 20)

# Get transaction history
eT3Cash.get_transaction_history()
