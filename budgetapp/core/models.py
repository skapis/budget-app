import uuid
from datetime import datetime as dt
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db.models import Sum


class TransactionType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    categoryId = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=255)
    type = models.ForeignKey(to=TransactionType, on_delete=models.SET_NULL, null=True)
    icon = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = 'Currencies'


class Wallet(models.Model):
    walletId = models.UUIDField(default=uuid.uuid4)
    owner = models.OneToOneField(to=User, on_delete=models.CASCADE)
    currency = models.ForeignKey(to=Currency, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.owner.username} - {self.currency.code}"

    def total_transactions(self, m=dt.today().month, y=dt.today().year):
        # this method returns number of transactions in current month and year
        transactions = Transaction.objects.filter(wallet=self, date__month__lte=m, date__month__gte=m,
                                                  date__year__lte=y, date__year__gte=y)
        return transactions.count()

    def balance(self, m=dt.today().month, y=dt.today().year):
        incomes = self.incomes(m, y)
        expenses = self.expenses(m, y)
        return incomes - expenses

    def transactions(self, m=dt.today().month, y=dt.today().year):
        return Transaction.objects.filter(wallet=self, date__month__lte=m, date__month__gte=m, date__year__lte=y,
                                          date__year__gte=y)

    def expenses(self, m=dt.today().month, y=dt.today().year):
        expenses = Transaction.objects.filter(wallet=self, date__month__lte=m, date__month__gte=m,
                                              date__year__lte=y, date__year__gte=y,
                                              type=TransactionType.objects.get(pk=2))  # 2 is id for Expense
        expenses_sum = expenses.aggregate(sum=Sum('amount'))['sum']
        if expenses_sum:
            return expenses_sum
        return 0

    def incomes(self, m=dt.today().month, y=dt.today().year):
        incomes = Transaction.objects.filter(wallet=self, date__month__lte=m, date__month__gte=m,
                                             date__year__lte=y, date__year__gte=y,
                                             type=TransactionType.objects.get(pk=1))  # 1 is id for Income
        income_sum = incomes.aggregate(sum=Sum('amount'))['sum']
        if income_sum:
            return income_sum
        return 0

    @property
    def all_transactions(self):
        transactions = Transaction.objects.filter(wallet=self)
        return transactions


class Transaction(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(to=Wallet, on_delete=models.CASCADE)
    transactionId = models.UUIDField(default=uuid.uuid4, unique=True)
    type = models.ForeignKey(to=TransactionType, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    month_label = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField()
    createdAt = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.owner.username} - {self.transactionId}"

    def save(self, *args, **kwargs):
        year = dt.strptime(str(self.date), '%Y-%m-%d').year
        month = dt.strptime(str(self.date), '%Y-%m-%d').month
        if month < 10:
            month = f"0{month}"
        self.month_label = f"{year}-{month}"
        super(Transaction, self).save(*args, **kwargs)

