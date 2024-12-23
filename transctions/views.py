
from rest_framework import status
from rest_framework.response import Response
from .models import User, Transaction
from .serializers import UserSerializer, TransactionSerializer
from decimal import Decimal
from rest_framework.authentication import BasicAuthentication , TokenAuthentication 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import AccessToken

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
import json

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

# Home page view
# @api_view(['GET'])
# def home(request):
#     return Response({'message': 'Welcome to the API Home'})



# # Deposit view
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

# # Withdraw view
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

# # Pay Bill view
VALID_BILL_TYPES = ['water', 'gas', 'electricity', 'internet']
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay_bill(request):
    # phone_number = request.data.get('phone').strip()
    user = request.user
    bill_name = request.data.get('bill_name') ## this line for front with java switch to under line 
    # bill_name = request.data.get('bill_name').strip()
    amount = Decimal(request.data.get('amount'))
    # user = User.objects.get(phone_number=phone_number)
        # Check if bill_name is empty or not in the allowed types
    if not bill_name or bill_name not in VALID_BILL_TYPES:
        return Response({'error': 'Invalid bill type. Only water, gas, electricity, and internet are allowed.'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        user.pay_bill(amount)
        transaction = Transaction.objects.create(sender=user, amount=amount, transaction_type=f'Bill Payment ({bill_name})')
        return Response({'message': f'{user.name} paid {amount} for {bill_name}. New balance is {user.balance}'})
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# # Buy Airtime view
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

# # Transfer view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer(request):
    user = request.user
    recipient_phone = request.data.get('recipient_phone')
    amount = Decimal(request.data.get('amount'))

    try:
        recipient = User.objects.get(phone_number=recipient_phone)
    except User.DoesNotExist:
        return Response({'error': 'Recipient not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Prevent transferring to self
    if user.phone_number == recipient_phone:
        return Response({'error': 'You cannot transfer to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

    if user.balance >= amount:
        user.withdraw(amount)
        recipient.deposit(amount)
        transaction = Transaction.objects.create(sender=user, recipient=recipient, amount=amount, transaction_type='Transfer')
        return Response({'message': f'Transferred {amount} from {user.name} to {recipient.name}.',
                         'recipient_name': recipient.name })
    else:
        return Response({'error': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)

# # Check Balance view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def balance(request):
    user = request.user  # Use the authenticated user from the request

    # Return the user's balance
    return Response({'message': f"{user.name}'s balance is {user.balance}.",'balance':user.balance})

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
            'user':{
                'name': user.name,  # Assuming 'name' field exists in the User model
            }
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes(IsAuthenticated)
def logout(request):
    # No need to handle refresh tokens or blacklisting, just return a response
    return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

##########################API front vue#########################3
def home(request):
    return render(request, 'home.html')

# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])
# def login_user(request):
#     if request.method == 'POST':
#         phone_number = request.data.get('phone_number')
#         password = request.data.get('password')

#         user = authenticate(request, phone_number=phone_number, password=password)
#         if user:
#             access_token = AccessToken.for_user(user)
#             return JsonResponse({'access': str(access_token), 'user': {'name': user.name}})
#         else:
#             return JsonResponse({'error': 'Invalid credentials'}, status=400)

#     return render(request, 'login.html')  # Render login form

# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     if request.method == 'POST':
#         phone_number = request.data.get('phone_number')
#         password = request.data.get('password')
#         name = request.data.get('name')

#         if User.objects.filter(phone_number=phone_number).exists():
#             return JsonResponse({'error': 'Phone number already registered.'}, status=400)

#         user = User.objects.create(phone_number=phone_number, name=name)
#         user.set_password(password)
#         user.save()

#         access_token = AccessToken.for_user(user)
#         return JsonResponse({'access': str(access_token)}, status=201)

#     return render(request, 'register.html')  # Render register form

# # from django.views.decorators.cache import cache_control

# # @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def dashboard_view(request):
#     return render(request, 'dashboard.html')

# def deposit_page(request):
#     return render(request, 'deposit.html')

# def withdraw_page(request):
#     return render(request, 'withdraw.html')

# def payBill_page(request):
#     return render(request, 'payBill.html')

# def buyAirtime_page(request):
#     return render(request, 'buyAirtime.html')

# def transfer_page(request):
#     return render(request, 'transfer.html')

# def transactionHistory_page(request):
#     return render(request, 'transactionHistory.html')

# def balance_page(request):
#     return render(request, 'balance.html')

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def transactionHistory(request):
#     user = request.user
#     transactions = Transaction.objects.filter(sender=user)  # Fetch transactions for the authenticated user

#     # Create a list to hold transaction data
#     transaction_data = []

#     for transaction in transactions:
#         transaction_data.append({
#             'date': transaction.date,  # Assuming you have a timestamp field `created_at`
#             'transaction_type': transaction.transaction_type,
#             'amount': transaction.amount,
#             'recipient': transaction.recipient.name if transaction.recipient else None,  # If you have a recipient field
#             'balance_after': user.balance  # Assuming you have a balance attribute on your user model
#         })

#     return Response({'transactions': transaction_data}, status=status.HTTP_200_OK)