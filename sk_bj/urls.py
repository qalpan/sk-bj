from django.contrib import admin
from django.urls import path
from django.contrib.auth import get_user_model

def create_admin():
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'pass1234')

# Сайт қосылғанда админ жасайды
try:
    create_admin()
except:
    pass

urlpatterns = [
    path('admin/', admin.site.urls),
]
