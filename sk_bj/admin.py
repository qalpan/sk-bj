from django.contrib import admin
from .models import Property, BankPayment

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('address', 'account_number', 'area', 'debt_maint', 'debt_cap')
    search_fields = ('address', 'account_number')
    list_filter = ('area',)

@admin.register(BankPayment)
class BankPaymentAdmin(admin.ModelAdmin):
    list_display = ('property', 'amount', 'payer_name', 'date')
    date_hierarchy = 'date'
