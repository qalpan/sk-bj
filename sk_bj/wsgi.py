import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sk_bj.settings')
application = get_wsgi_application()

# Админді автоматты түрде жасау
try:
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'pass1234')
        print("Superuser created successfully!")
except Exception as e:
    print(f"Error creating superuser: {e}")
