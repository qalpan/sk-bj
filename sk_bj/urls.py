from django.contrib import admin
from django.urls import path
# 'core' сөзін өзіңіздің нақты папкаңыздың атына ауыстырыңыз
# Мысалы, егер views.py файлыңыз 'sk_bj' ішінде болса:
from sk_bj import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Дұрысталды: admin.site.urls
    path('login/', views.resident_auth, name='resident_auth'),
    path('import-json/', views.import_from_json, name='import_json'),
    path('signup-special-access/', views.signup, name='signup'),
    path('import-data/', views.import_data, name='import_data'),
    path('upload-bank/', views.upload_bank, name='upload_bank'),
]
