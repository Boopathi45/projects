from django.urls import path

from Accounts.views import *

appname = 'PropertyApp'
urlpatterns = [
    path('signup/', Signup.as_view()),
    path('signin/', Signin.as_view()),
    path('wallet_info/', WalletListView.as_view()),
    path('wallet_recharge/', WalletRechargeView.as_view()),
    path('editors/', EditorsView.as_view())
]