from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_admin(sender, **kwargs):
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'pass1234')
        print("Админ жасалды!")

class SkBjConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sk_bj'

    def ready(self):
        post_migrate.connect(create_admin, sender=self)
