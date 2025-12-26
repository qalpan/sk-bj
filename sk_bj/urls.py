from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Тек жұмыс істейтін жаңа жолдарды қалдырамыз
    path('admin-panel/', TemplateView.as_view(template_name="tөlemesep_smart.html"), name='admin_panel'),
    path('api/data/', views.api_manager, name='api_data'),
    path('pater/<str:apt_id>/', views.api_manager, name='pater_detail'),
]
