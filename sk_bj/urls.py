from django.urls import path
from django.views.generic import TemplateView
from . import views  # Өз views.py файлыңызды импорттау

urlpatterns = [
    # Админ панелі (бұл файл templates/ қалтасында тұруы керек)
    path('admin-panel/', TemplateView.as_view(template_name="tөlemesep_smart.html"), name='admin_panel'),
    
    # API: Деректерді алу және сақтау (екі қызметті бір views атқарады)
    path('api/data/', views.api_manager, name='api_data'),
    
    # Тұрғынның жеке бөлмесі
    # Мысалы: /pater/9a/ немесе /pater/15/
    path('pater/<str:apt_id>/', views.api_manager, name='pater_detail'),
]
