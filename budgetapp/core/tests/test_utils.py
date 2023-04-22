from datetime import datetime as dt
from django.test import TestCase
from core.models import Wallet, Currency, Category, Transaction, TransactionType
from django.contrib.auth.models import User
from core.utils import get_transactions_years, transactions_by_time, transactions_by_category


class TestUtilsMethods(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='TestUser1')
        self.user2 = User.objects.create_user(username='test2', password='TestUser1')
        self.currency = Currency.objects.create(code='EUR', symbol='€', name='Euro')
        self.wallet = Wallet.objects.create(
            walletId='efac7636-ad71-4d33-a0fa-72cd0597dd8d',
            owner=User.objects.get(username='test'),
            currency=Currency.objects.get(code='EUR'),
        )
        self.empty_wallet = Wallet.objects.create(
            walletId='efac7636-ad71-4d33-a0fa-72cd0597dd8d',
            owner=User.objects.get(username='test2'),
            currency=Currency.objects.get(code='EUR'),
        )
        self.exp_type = TransactionType.objects.create(pk=2, name_en='Expense')
        self.inc_type = TransactionType.objects.create(pk=1, name_en='Income')
        self.inc_category = Category.objects.create(name='Salary', name_en='Salary', type=self.inc_type)
        self.exp_category = Category.objects.create(name='Home', name_en='Home', type=self.exp_type)
        self.exp_category_fun = Category.objects.create(name='Entertainment', name_en='Entertainment',
                                                        type=self.exp_type)
        self.transaction1 = Transaction.objects.create(
            wallet=self.wallet,
            owner=self.wallet.owner,
            type=self.exp_type,
            date='2022-03-06',
            category=self.exp_category,
            amount=5000,
            description='Pay Rent'
        )
        self.transaction2 = Transaction.objects.create(
            wallet=self.wallet,
            owner=self.wallet.owner,
            type=self.exp_type,
            date='2021-03-06',
            category=self.exp_category_fun,
            amount=6000,
            description='Electronics'
        )
        self.transaction3 = Transaction.objects.create(
            wallet=self.wallet,
            owner=self.wallet.owner,
            type=self.inc_type,
            date='2023-03-06',
            category=self.inc_category,
            amount=20000,
            description='Salary'
        )
        self.transaction4 = Transaction.objects.create(
            wallet=self.wallet,
            owner=self.wallet.owner,
            type=self.inc_type,
            date='2023-03-06',
            category=self.inc_category,
            amount=20000,
            description='Salary'
        )
        self.transaction4 = Transaction.objects.create(
            wallet=self.wallet,
            owner=self.wallet.owner,
            type=self.inc_type,
            date='2023-03-06',
            category=self.inc_category,
            amount=20000,
            description='Salary'
        )

    def test_get_transactions_years(self):
        years = get_transactions_years(self.wallet)
        years_empty = get_transactions_years(self.empty_wallet)
        self.assertEqual(len(years), 3)
        # test if wallet is empty
        self.assertEqual(years_empty[0], dt.today().year)

    def test_transaction_by_time(self):
        data = transactions_by_time(self.wallet, 'month')
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)
        income_sum = list(filter(lambda x: x['month_label'] == '2023-03', data))
        self.assertEqual(income_sum[0]['sum'], 60000)
        empty_data = transactions_by_time(self.empty_wallet, 'month')
        self.assertEqual(len(empty_data), 0)

    def test_transactions_by_category(self):
        data = transactions_by_category(self.wallet, 1, '2023-03', 'en')
        self.assertEqual(data['Salary'], 60000)

