from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_admin(sender, **kwargs):
    from django.contrib.auth.models import User
    # Базада 'admin' бар-жоғын тексереді, жоқ болса жасайды
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'pass1234')

class SkBjConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sk_bj'

    def ready(self):
        # post_migrate — база дайын болғанда ғана іске қосылатын сигнал
        post_migrate.connect(create_admin, sender=self)
