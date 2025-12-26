from django.urls import path
from . import views

urlpatterns = [
    path('api/data/', views.api_manager, name='api_data'),
    path('pater/<str:apt_id>/', views.api_manager, name='pater_page'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]
