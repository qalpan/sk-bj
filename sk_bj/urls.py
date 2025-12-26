from django.contrib import admin
from django.urls import path
from sk_bj import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup-special-access/', views.signup, name='signup'),
    path('import-data/', views.import_json_data, name='import_data'), # ОСЫ ЖОЛ
    path('upload-bank/', views.upload_bank_file, name='upload_bank'),
]
