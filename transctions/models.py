from django.db import models
from django.utils import timezone
from decimal import Decimal

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def deposit(self, amount):
        self.balance += Decimal(amount)  # Ensure amount is Decimal
        self.save()

    def withdraw(self, amount):
        if Decimal(amount) > self.balance:
            raise ValueError("Insufficient balance!")
        self.balance -= Decimal(amount)  # Ensure amount is Decimal
        self.save()

    def pay_bill(self, amount):
        self.withdraw(amount)

    def buy_airtime (self, amount):
        self.withdraw(amount)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name="sent_transactions", on_delete=models.CASCADE, null=True)
    recipient = models.ForeignKey(User, related_name="received_transactions", on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_type}: {self.sender} -> {self.recipient} | {self.amount}"