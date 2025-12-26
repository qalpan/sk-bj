from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_admin(sender, **kwargs):
    from django.contrib.auth.models import User
    # Егер 'admin' логині жоқ болса, оны жасайды
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'pass1234')
        print("Админ сәтті жасалды!")

class SkBjConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sk_bj'

    def ready(self):
        # post_migrate сигналы база дайын болғанда іске қосылады
        post_migrate.connect(create_admin, sender=self)
