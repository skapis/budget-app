from .models import Wallet, Transaction
from datetime import datetime as dt
from django.db.models import Sum


# this method return a list of unique years of user transactions
def get_transactions_years(wallet):
    transactions = wallet.all_transactions

    if transactions.count() != 0:
        dates_list = transactions.values_list('date', flat=True).distinct()
        years = list(set(list(map(lambda item: item.year, dates_list))))
        years.sort(reverse=True)
        return years

    return [dt.today().year]


def transactions_by_time(wallet, period):
    transactions = wallet.all_transactions
    if period == 'month':
        period = 'month_label'
    else:
        period = 'date__year'
    if transactions.count() != 0:
        data = transactions.values(period, 'type__name').annotate(sum=Sum('amount'))
        return list(data)

    return []


def transactions_by_category(wallet, typ, month, lang):
    transactions = Transaction.objects.filter(wallet=wallet, month_label=month, type__pk=typ)
    if transactions.count() != 0:
        category = transactions.values_list(f'category__name_{lang}').annotate(sum=Sum('amount'))
        return dict(category)
    return []



