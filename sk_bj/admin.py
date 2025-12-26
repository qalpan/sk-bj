from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(ImportExportModelAdmin): # Осы жерін ауыстырдық
    list_display = ('address', 'owner_name', 'area')
