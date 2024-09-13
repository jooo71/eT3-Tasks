from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name='transfer'),
    path('balance/', views.balance, name='balance'),
    path('history/', views.transaction_history, name='history'),
    path('pay_bill/', views.pay_bill, name='pay_bill'),
    path('buy_airtime/', views.buy_airtime, name='buy_airtime'),
]