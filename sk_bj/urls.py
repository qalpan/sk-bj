from django.contrib import admin
from django.urls import path
from . import views  # Осыны қосуды ұмытпаңыз

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup-special-access/', views.signup, name='signup'),
]
