from django.contrib import admin
from .models import Property, BankPayment

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('apartment_id', 'account_number', 'address', 'area') # Мұндағы аттар модельдегімен бірдей болуы тиіс
    search_fields = ('apartment_id', 'account_number')

@admin.register(BankPayment)
class BankPaymentAdmin(admin.ModelAdmin):
    list_display = ('property', 'amount', 'payer_name', 'payment_date')
