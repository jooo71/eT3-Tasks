# from django.shortcuts import render, get_object_or_404, redirect
# from .models import User, Transaction
# from decimal import Decimal
# from django.utils import timezone
# from django.contrib.auth import authenticate, login
# from django.contrib import messages
# from rest_framework.permissions import IsAuthenticated ,IsAdminUser
# from rest_framework import generics
# from .models import User, Transaction
# from .serializers import TransactionSerializer
# from rest_framework.response import Response
# from rest_framework.views import APIView
# # from rest_framework.permissions import IsAuthenticated
# # from .models import User, Transaction
# from django.contrib.auth.decorators import login_required

# # Home page view
# def home(request):
#     return render(request, 'home.html')

# # Deposit view
# def deposit(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone')
#         amount = Decimal(request.POST.get('amount'))  # Convert amount to Decimal
#         user = get_object_or_404(User, phone_number=phone_number)
#         user.deposit(amount)  # Deposit amount as Decimal
#         Transaction.objects.create(sender = user, recipient=None, amount=amount, transaction_type='deposit')
#         message = f"Deposited {amount} to {user.name}. New balance: {user.balance}"
#         return render(request, 'home.html', {'message': message})
#     return redirect('home')

# # Withdraw view
# def withdraw(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone')
#         amount = Decimal(request.POST.get('amount'))  # Convert amount to Decimal
#         user = get_object_or_404(User, phone_number=phone_number)
#         try:
#             user.withdraw(amount)  # Withdraw amount as Decimal
#             message = f"Withdrew {amount} from {user.name}. New balance: {user.balance}"
#             Transaction.objects.create(sender = user, recipient=None, amount=amount, transaction_type='withdraw')
#         except ValueError as e:
#             message = str(e)
#         return render(request, 'home.html', {'message': message})
#     return redirect('home')

# def pay_bill(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone').strip()
#         bill_name = request.POST.get('bill_name').strip()
#         amount = Decimal(request.POST.get('amount'))
#         user = get_object_or_404(User, phone_number=phone_number)
#         try:
#             user.pay_bill(amount)  # Withdraw amount as Decimal
#             message = f"{user.name} paid {amount} for {bill_name}. New balance is {user.balance}"
#             Transaction.objects.create(sender = user, recipient=None, amount=amount, transaction_type=f'Bill Payment ({bill_name})')
#         except ValueError as e:
#             message = str(e)
#         return render(request, 'home.html', {'message': message})
#     return redirect('home')

# def buy_airtime(request):
#     if request.method == 'POST':
#         phone_number = request.POST.get('phone').strip()
#         amount = Decimal(request.POST.get('amount'))
#         user = get_object_or_404(User, phone_number=phone_number)
#         try:
#             user.buy_airtime(amount)  # Withdraw amount as Decimal
#             message = f"Bought {amount} worth of airtime. New balance: {user.balance}"
#             Transaction.objects.create(sender = user, recipient=None, amount=amount, transaction_type=f'airtime Payment ')
#         except ValueError as e:
#             message = str(e)
#         return render(request, 'home.html', {'message': message})
#     return redirect('home')        
        

# # Transfer view
# def transfer(request):
#     if request.method == 'POST':
#         sender_phone = request.POST.get('sender_phone')
#         recipient_phone = request.POST.get('recipient_phone')
#         amount = Decimal(request.POST.get('amount'))  # Convert amount to Decimal

#         sender = get_object_or_404(User, phone_number=sender_phone)
#         recipient = get_object_or_404(User, phone_number=recipient_phone)

#         if sender.balance >= amount:
#             sender.withdraw(amount)
#             recipient.deposit(amount)
#             Transaction.objects.create(sender=sender, recipient=recipient, amount=amount, transaction_type='Transfer')
#             message = f"Transferred {amount} from {sender.name} to {recipient.name}."
#         else:
#             message = "Insufficient balance."
#         return render(request, 'home.html', {'message': message})
#     return redirect('home')

# # Check balance view
# def balance(request):
#     if request.method == 'GET':
#         phone_number = request.GET.get('phone')
#         user = get_object_or_404(User, phone_number=phone_number)
#         message = f"{user.name}'s balance is {user.balance}."
#         return render(request, 'home.html', {'message': message})
#     return redirect('home')

# # Transaction history view

# def transaction_history(request):
#     if request.method == 'GET':
#         phone_number = request.GET.get('phone')
#         user = get_object_or_404(User, phone_number=phone_number)
#         transactions = Transaction.objects.filter(sender=user) | Transaction.objects.filter(recipient=user)
#         return render(request, 'history.html', {'transactions': transactions})
#     return redirect('home')


        

from rest_framework import status
from rest_framework.response import Response
from .models import User, Transaction
from .serializers import UserSerializer, TransactionSerializer
from decimal import Decimal
from rest_framework.authentication import BasicAuthentication , TokenAuthentication 
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import AccessToken

# Home page view
@api_view(['GET'])
def home(request):
    return Response({'message': 'Welcome to the API Home'})

# Deposit view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit(request):
    print("Request User:", request.user)  # Debugging line
    user = request.user
    amount = Decimal(request.data.get('amount'))
    # user = User.objects.get(phone_number=phone_number)
    user.deposit(amount)
    transaction = Transaction.objects.create(sender=user, amount=amount, transaction_type='deposit')
    return Response({'message': f'Deposited {amount} to {user.name}. New balance: {user.balance}'})

# Withdraw view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw(request):
    # Use the authenticated user from the request
    user = request.user
    amount = Decimal(request.data.get('amount'))

    try:
        # Attempt to withdraw the amount
        user.withdraw(amount)
        Transaction.objects.create(sender=user, amount=amount, transaction_type='withdraw')
        return Response({'message': f'Withdrew {amount} from {user.name}. New balance: {user.balance}'})
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Pay Bill view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay_bill(request):
    # phone_number = request.data.get('phone').strip()
    user = request.user
    bill_name = request.data.get('bill_name').strip()
    amount = Decimal(request.data.get('amount'))
    # user = User.objects.get(phone_number=phone_number)
    try:
        user.pay_bill(amount)
        transaction = Transaction.objects.create(sender=user, amount=amount, transaction_type=f'Bill Payment ({bill_name})')
        return Response({'message': f'{user.name} paid {amount} for {bill_name}. New balance is {user.balance}'})
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Buy Airtime view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_airtime(request):
    user = request.user
    amount = Decimal(request.data.get('amount'))
    # user = User.objects.get(phone_number=phone_number)
    try:
        user.buy_airtime(amount)
        transaction = Transaction.objects.create(sender=user, amount=amount, transaction_type='Airtime Payment')
        return Response({'message': f'Bought {amount} worth of airtime. New balance: {user.balance}'})
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Transfer view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer(request):
    user = request.user
    recipient_phone = request.data.get('recipient_phone')
    amount = Decimal(request.data.get('amount'))

    # sender = User.objects.get(phone_number=sender_phone)
    recipient = User.objects.get(phone_number=recipient_phone)

    if user.balance >= amount:
        user.withdraw(amount)
        recipient.deposit(amount)
        transaction = Transaction.objects.create(sender=user, recipient=recipient, amount=amount, transaction_type='Transfer')
        return Response({'message': f'Transferred {amount} from {user.name} to {recipient.name}.'})
    else:
        return Response({'error': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)

# Check Balance view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def balance(request):
    user = request.user  # Use the authenticated user from the request

    # Return the user's balance
    return Response({'message': f"{user.name}'s balance is {user.balance}."})

# Transaction History view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request):
    user = request.user  # Get the authenticated user from the request

    # Fetch all transactions where the user is either the sender or recipient
    transactions = Transaction.objects.filter(sender=user) | Transaction.objects.filter(recipient=user)

    # Serialize the transactions
    serializer = TransactionSerializer(transactions, many=True)

    # Return the serialized data
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    name = request.data.get('name')

    # Check if all required fields are provided
    if phone_number is None or password is None or name is None:
        return Response({'error': 'Please provide phone number, name, and password.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the phone number already exists
    if User.objects.filter(phone_number=phone_number).exists():
        return Response({'error': 'Phone number already registered.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new user and hash the password using set_password
    user = User.objects.create(phone_number=phone_number, name=name)
    user.set_password(password)  # Ensure password is hashed
    user.save()

    # Generate only an access token for the new user
    access_token = AccessToken.for_user(user)

    return Response({
        'access': str(access_token),
    }, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')

    # Authenticate user
    user = authenticate(request, phone_number=phone_number, password=password)
    if user is not None:
        # Generate only an access token
        access_token = AccessToken.for_user(user)
        return Response({
            'access': str(access_token),
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
