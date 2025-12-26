from django.contrib import admin
from .models import Property, BankPayment

@admin.register(BankPayment)
class BankPaymentAdmin(admin.ModelAdmin):
    list_display = ('property', 'amount', 'payer_name', 'date')
    list_filter = ('date', 'property')
    # Бұл жерде сіз CSV-ді жүктейтін сілтеме қоса аласыз
