from django.contrib import admin
from django.urls import path
from core import views  # core — бұлттық папкаңыздың аты, егер басқаша болса соны жазыңыз

urlpatterns = [
    path('admin/', admin.site.site.urls),
    path('login/', views.resident_auth, name='resident_auth'), # ОСЫ ЖОЛДЫ ҚОСЫҢЫЗ
    path('signup-special-access/', views.signup, name='signup'),
    path('import-data/', views.import_data, name='import_data'),
    path('upload-bank/', views.upload_bank, name='upload_bank'),
]
