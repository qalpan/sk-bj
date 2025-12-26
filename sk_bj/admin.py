from django.contrib import admin
from .models import Tariff, Property, Invoice

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate', 'is_per_sqm')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('address', 'owner_name', 'area')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('property', 'month', 'total_amount')
