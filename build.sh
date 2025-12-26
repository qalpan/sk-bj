#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Админ жасауды қауіпсіз түрде іске қосу
python manage.py shell << END
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'pass1234')
        print('Админ жасалды!')
    else:
        print('Админ бұрыннан бар.')
except Exception as e:
    print(f'Қате: {e}')
END
