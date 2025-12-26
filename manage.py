#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sk_bj.settings')
    try:
        from django.core.management import execute_from_command_line
        # Админ жасау блогы осы жерде болуы керек
        from django.db import connection
        from django.contrib.auth.models import User
        
        # База дайын болғанда ғана админ жасаймыз
        execute_from_command_line(['manage.py', 'migrate']) # Базаны алдын ала дайындау
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'pass1234')
            print("Админ сәтті жасалды: Логин - admin, Пароль - pass1234")
            
    except ImportError as exc:
        raise ImportError("Django табылмады!") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
