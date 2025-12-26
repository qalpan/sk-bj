from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Бұрынғы бар жолдар (өшірмеңіз, қала берсін)
    path('login/', views.resident_auth, name='resident_auth'),
    path('import-json/', views.import_json, name='import_json'),
    path('signup-special-access/', views.signup, name='signup'),
    path('upload-bank/', views.upload_bank, name='upload_bank'),

    # БІЗДІҢ ЖАҢА ЫҚШАМДАЛҒАН ЖОЛДАР:
    # Әкімші панелі
    path('admin-panel/', TemplateView.as_view(template_name="tөlemesep_smart.html"), name='admin_panel'),
    
    # Ортақ API жолы (Алу және Сақтау)
    path('api/data/', views.api_manager, name='api_data'),
    
    # Тұрғынның түбіртегі (Мысалы: /pater/9a/)
    path('pater/<str:apt_id>/', views.api_manager, name='pater_detail'),
]
