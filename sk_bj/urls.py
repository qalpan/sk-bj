from django.contrib import admin
from django.urls import path
from sk_bj import views  # 'sk_bj' дегенді қосуды ұмытпаңыз

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup-special-access/', views.signup, name='signup'),
]
