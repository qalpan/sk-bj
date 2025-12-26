import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sk_bj.settings')
application = get_wsgi_application()

# Бұл бөлім админ аккаунтын мәжбүрлі түрде жасайды
try:
    from django.contrib.auth.models import User
    # Егер 'admin' логині жоқ болса, оны жаңадан жасайды
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'pass1234')
        print("Суперпайдаланушы сәтті жасалды!")
    else:
        # Егер бар болса, паролін жаңартады (ұмытып қалмас үшін)
        u = User.objects.get(username='admin')
        u.set_password('pass1234')
        u.save()
        print("Админ паролі жаңартылды!")
except Exception as e:
    print(f"Админ жасау кезінде қате шықты: {e}")
