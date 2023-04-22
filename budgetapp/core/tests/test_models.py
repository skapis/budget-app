from datetime import datetime as dt
from django.test import TestCase
from core.models import Wallet, Currency, Category, Transaction, TransactionType
from django.contrib.auth.models import User
from django.db.models.query import QuerySet


class TestWalletModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='TestUser1')
        self.currency = Currency.objects.create(code='EUR', symbol='€', name='Euro')
        self.wallet = Wallet.objects.create(
            walletId='efac7636-ad71-4d33-a0fa-72cd0597dd8d',
            owner=User.objects.get(username='test'),
            currency=Currency.objects.get(code='EUR'),
        )
        self.exp_type = TransactionType.objects.create(pk=2, name_en='Expense')
        self.inc_type = TransactionType.objects.create(pk=1, name_en='Income')
        self.inc_category = Category.objects.create(name='Salary', type=self.inc_type)
        self.exp_category = Category.objects.create(name='Home', type=self.exp_type)
        self.transaction1 = Transaction.objects.create(
            wallet=self.wallet,
            owner=self.wallet.owner,
            type=self.exp_type,
            date=dt.today().date(),
            category=self.exp_category,
            amount=5000,
            description='Pay Rent'
        )
        self.transaction2 = Transaction.objects.create(
            wallet=self.wallet,
            owner=self.wallet.owner,
            type=self.exp_type,
            date=dt.today().date(),
            category=self.exp_category,
            amount=6000,
            description='Electronics'
        )
        self.transaction3 = Transaction.objects.create(
            wallet=self.wallet,
            owner=self.wallet.owner,
            type=self.inc_type,
            date=dt.today().date(),
            category=self.inc_category,
            amount=20000,
            description='Salary'
        )

    def test_create_transaction(self):
        transaction = Transaction.objects.create(
            wallet=self.wallet,
            owner=self.wallet.owner,
            type=self.exp_type,
            date=dt.today().date(),
            category=self.exp_category,
            amount=5000,
            description='Pay Rent'
        )
        self.assertEqual(transaction.type.name_en, 'Expense')
        self.assertEqual(transaction.amount, 5000)
        self.assertIsNotNone(transaction)

    def test_total_transactions(self):
        self.assertEqual(self.wallet.total_transactions(), 3)

    def test_wallet_balance(self):
        self.assertEqual(self.wallet.balance(), 9000)

    def test_wallet_transactions(self):
        self.assertIsInstance(self.wallet.transactions(), QuerySet)

