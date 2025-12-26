import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sk_bj.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'pass1234')
    print("Админ сәтті жасалды!")
else:
    print("Админ бұрыннан бар.")
