from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Wallet, Currency, Category, Transaction, TransactionType
from django.contrib import messages
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.utils.translation import get_language
from .utils import get_transactions_years, transactions_by_time, transactions_by_category


def home(request):
    return render(request, 'home.html')


@login_required(login_url='/auth/login')
def dashboard(request):
    if request.method == 'GET':
        user = request.user
        wallet = Wallet.objects.get(owner=user)
        month = request.GET.get('month', None)
        year = request.GET.get('year', None)

        if month and year:
            trans_count = wallet.total_transactions(m=month, y=year)
            incomes = wallet.incomes(m=month, y=year)
            expenses = wallet.expenses(m=month, y=year)
            balance = wallet.balance(m=month, y=year)
            trans = wallet.transactions(m=month, y=year)
        else:
            trans_count = wallet.total_transactions()
            incomes = wallet.incomes()
            expenses = wallet.expenses()
            balance = wallet.balance()
            trans = wallet.transactions()

        context = {
            'wallet': wallet,
            'transactionCount': trans_count,
            'incomes': incomes,
            'expenses': expenses,
            'balance': balance,
            'transactions': trans,
            'years': get_transactions_years(wallet)
        }
        return render(request, 'budget/dashboard.html', context)


@login_required(login_url='/auth/login')
def transactions(request):
    wallet = Wallet.objects.get(owner=request.user)
    month = request.GET.get('month', None)
    year = request.GET.get('year', None)
    if month and year:
        trans = wallet.transactions(m=month, y=year)
    else:
        trans = wallet.all_transactions
    context = {
        'transactions': trans,
        'years': get_transactions_years(wallet)
    }
    return render(request, 'budget/transactions.html', context)


@login_required(login_url='/auth/login')
def transactions_by_period(request):
    wallet = Wallet.objects.get(owner=request.user)
    period = request.GET.get('period', None)
    if period:
        return JsonResponse({'data': transactions_by_time(wallet, period)}, status=200)
    return JsonResponse({'message': 'Missing required url parameters'}, status=404)


@login_required(login_url='/auth/login')
def category_transactions(request):
    wallet = Wallet.objects.get(owner=request.user)
    typ = request.GET.get('type', None)
    month = request.GET.get('month', None)
    lang = get_language()
    if typ and month:
        return JsonResponse({'data': transactions_by_category(wallet, typ, month, lang)})
    return JsonResponse({'message': 'Missing required url parameters'}, status=404)


def categories(request):
    if request.method == 'GET':
        resp = {
            'income': list(Category.objects.filter(type=TransactionType.objects.get(pk=1)).values()),
            'expense': list(Category.objects.filter(type=TransactionType.objects.get(pk=2)).values())
        }
        return JsonResponse({'categories': resp}, safe=False, status=200)
    return JsonResponse({'message': 'not allowed method'}, status=405)


@login_required(login_url='/auth/login')
def transaction(request):
    if request.method == 'POST':
        data = request.POST
        wallet = request.user.wallet
        typ = TransactionType.objects.get(pk=data['type'])
        category = Category.objects.get(categoryId=data['category'])
        date = data['date']
        amount = data['amount']
        description = data['description']

        if wallet and typ and category and date and amount:
            if typ.pk == category.type.pk:
                Transaction.objects.create(wallet=wallet, owner=wallet.owner, type=typ, category=category, date=date,
                                           amount=amount, description=description)
                messages.success(request, _('Transaction was created'))
                return redirect(request.META['HTTP_REFERER'])
            messages.error(request, _('Different transaction type than category type'))
            return redirect(request.META['HTTP_REFERER'])
        messages.error(request, _('All required fields must be filled'))
        return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/auth/login')
def delete_transaction(request, transaction_id):
    trans = Transaction.objects.get(transactionId=transaction_id)
    trans.delete()
    messages.success(request, _('Transaction was removed'))
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/auth/login')
def edit_transaction(request, transaction_id):
    if request.method == 'GET':
        trans = Transaction.objects.get(transactionId=transaction_id)
        context = {
            'transaction': trans,
            'types': TransactionType.objects.all()
        }
        return render(request, 'budget/transactionDetail.html', context)

    if request.method == 'POST':
        trans = Transaction.objects.get(transactionId=transaction_id)
        data = request.POST
        typ = TransactionType.objects.get(pk=data['type'])
        category = Category.objects.get(categoryId=data['category'])
        date = data['date']
        amount = data['amount']

        if typ and category and date and amount:
            if typ.pk == category.type.pk:
                trans.typ = typ
                trans.category = category
                trans.date = date
                trans.amount = amount
                trans.save()

                messages.success(request, _('Transaction was changed'))
                return redirect(request.META['HTTP_REFERER'])
            messages.error(request, _('Different transaction type than category type'))
            return redirect(request.META['HTTP_REFERER'])
        messages.error(request, _('All required fields must be filled'))
        return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/auth/login')
def user_wallet(request):
    user = request.user
    if request.method == 'GET':
        context = {
            'wallet': user.wallet,
            'currencies': Currency.objects.all()
        }
        return render(request, 'budget/userWallet.html', context)
    if request.method == 'POST':
        currency = request.POST['currency']
        user.wallet.currency = Currency.objects.get(code=currency)
        user.wallet.save()
        messages.success(request, _('Currency was changed'))
        return redirect('account')
    return JsonResponse({'message': 'not allowed method'}, status=405)

