from django.contrib import admin
from django.urls import path
from sk_bj import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.resident_auth, name='resident_auth'),
    path('import-json/', views.import_from_json, name='import_json'), # Локальді файлды жүктеу беті
    path('signup-special-access/', views.signup, name='signup'),
    path('upload-bank/', views.upload_bank_file, name='upload_bank'), # Функция атын views-қа сәйкестендірдік
]
