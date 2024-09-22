# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('deposit/', views.deposit, name='deposit'),
#     path('withdraw/', views.withdraw, name='withdraw'),
#     path('transfer/', views.transfer, name='transfer'),
#     path('balance/', views.balance, name='balance'),
#     path('history/', views.transaction_history, name='history'),
#     path('pay_bill/', views.pay_bill, name='pay_bill'),
#     path('buy_airtime/', views.buy_airtime, name='buy_airtime'),
#     # path('', views.user_login, name='login'),

# ]

from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', views.home, name='api-home'),
    path('api/deposit/', views.deposit, name='api-deposit'),
    path('api/withdraw/', views.withdraw, name='api-withdraw'),
    path('api/pay-bill/', views.pay_bill, name='api-pay-bill'),
    path('api/buy-airtime/', views.buy_airtime, name='api-buy-airtime'),
    path('api/transfer/', views.transfer, name='api-transfer'),
    path('api/balance/', views.balance, name='api-balance'),
    path('api/transaction-history/', views.transaction_history, name='api-transaction-history'),
    path('api/register/', views.register_user, name='register_user'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
