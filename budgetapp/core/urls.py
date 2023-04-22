from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('dashboard', dashboard, name='dashboard'),
    path('account', user_wallet, name='account'),
    path('categories', categories, name='categories'),
    path('transactions', transactions, name='transactions'),
    path('transaction', transaction, name='transaction'),
    path('transaction/delete/<uuid:transaction_id>', delete_transaction, name='del_transaction'),
    path('transaction/detail/<uuid:transaction_id>', edit_transaction, name='edit_transaction'),
    path('transactions/time', transactions_by_period),
    path('transactions/category', category_transactions)
]
