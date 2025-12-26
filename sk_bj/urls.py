from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Әкімші панелі
    path('admin-panel/', TemplateView.as_view(template_name="tөlemesep_smart.html"), name='admin_panel'),
    
    # Ортақ API жолы (Алу және Сақтау)
    path('api/data/', views.api_manager, name='api_data'),
    
    # Тұрғынның түбіртегі (Мысалы: /pater/9a/)
    path('pater/<str:apt_id>/', views.api_manager, name='pater_detail'),
]
