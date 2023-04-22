from django.contrib import admin
from .models import Currency, Wallet, TransactionType, Transaction, Category
from modeltranslation.admin import TranslationAdmin


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name', 'type', 'icon')


@admin.register(Transaction)
class TransactionDetail(admin.ModelAdmin):
    list_display = ('owner', 'wallet', 'type', 'category')


admin.site.register(Currency)
admin.site.register(Wallet)
admin.site.register(TransactionType)


