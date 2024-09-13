from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Transaction
from decimal import Decimal
# Home page view
def home(request):
    return render(request, 'home.html')

# Deposit view
def deposit(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        amount = Decimal(request.POST.get('amount'))  # Convert amount to Decimal
        user = get_object_or_404(User, phone_number=phone_number)
        user.deposit(amount)  # Deposit amount as Decimal
        Transaction.objects.create(sender = user, recipient=None, amount=amount, transaction_type='deposit')
        message = f"Deposited {amount} to {user.name}. New balance: {user.balance}"
        return render(request, 'home.html', {'message': message})
    return redirect('home')

# Withdraw view
def withdraw(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        amount = Decimal(request.POST.get('amount'))  # Convert amount to Decimal
        user = get_object_or_404(User, phone_number=phone_number)
        try:
            user.withdraw(amount)  # Withdraw amount as Decimal
            message = f"Withdrew {amount} from {user.name}. New balance: {user.balance}"
            Transaction.objects.create(sender = user, recipient=None, amount=amount, transaction_type='withdraw')
        except ValueError as e:
            message = str(e)
        return render(request, 'home.html', {'message': message})
    return redirect('home')

def pay_bill(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone').strip()
        bill_name = request.POST.get('bill_name').strip()
        amount = Decimal(request.POST.get('amount'))
        user = get_object_or_404(User, phone_number=phone_number)
        try:
            user.pay_bill(amount)  # Withdraw amount as Decimal
            message = f"{user.name} paid {amount} for {bill_name}. New balance is {user.balance}"
            Transaction.objects.create(sender = user, recipient=None, amount=amount, transaction_type=f'Bill Payment ({bill_name})')
        except ValueError as e:
            message = str(e)
        return render(request, 'home.html', {'message': message})
    return redirect('home')

def buy_airtime(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone').strip()
        amount = Decimal(request.POST.get('amount'))
        user = get_object_or_404(User, phone_number=phone_number)
        try:
            user.buy_airtime(amount)  # Withdraw amount as Decimal
            message = f"Bought {amount} worth of airtime. New balance: {user.balance}"
            Transaction.objects.create(sender = user, recipient=None, amount=amount, transaction_type=f'airtime Payment ')
        except ValueError as e:
            message = str(e)
        return render(request, 'home.html', {'message': message})
    return redirect('home')        
        

# Transfer view
def transfer(request):
    if request.method == 'POST':
        sender_phone = request.POST.get('sender_phone')
        recipient_phone = request.POST.get('recipient_phone')
        amount = Decimal(request.POST.get('amount'))  # Convert amount to Decimal

        sender = get_object_or_404(User, phone_number=sender_phone)
        recipient = get_object_or_404(User, phone_number=recipient_phone)

        if sender.balance >= amount:
            sender.withdraw(amount)
            recipient.deposit(amount)
            Transaction.objects.create(sender=sender, recipient=recipient, amount=amount, transaction_type='Transfer')
            message = f"Transferred {amount} from {sender.name} to {recipient.name}."
        else:
            message = "Insufficient balance."
        return render(request, 'home.html', {'message': message})
    return redirect('home')

# Check balance view
def balance(request):
    if request.method == 'GET':
        phone_number = request.GET.get('phone')
        user = get_object_or_404(User, phone_number=phone_number)
        message = f"{user.name}'s balance is {user.balance}."
        return render(request, 'home.html', {'message': message})
    return redirect('home')

# Transaction history view
def transaction_history(request):
    if request.method == 'GET':
        phone_number = request.GET.get('phone')
        user = get_object_or_404(User, phone_number=phone_number)
        transactions = Transaction.objects.filter(sender=user) | Transaction.objects.filter(recipient=user)
        return render(request, 'history.html', {'transactions': transactions})
    return redirect('home')
