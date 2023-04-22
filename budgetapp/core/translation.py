from modeltranslation.translator import translator, TranslationOptions
from .models import *


class CategoryTranslationOptions(TranslationOptions):
    fields = ['name']


class CurrencyTranslationOptions(TranslationOptions):
    fields = ['name']


class TransactionTypeTranslationOptions(TranslationOptions):
    fields = ['name']


translator.register(Category, CategoryTranslationOptions)
translator.register(Currency, CurrencyTranslationOptions)
translator.register(TransactionType, TransactionTypeTranslationOptions)
