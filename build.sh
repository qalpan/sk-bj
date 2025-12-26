#!/usr/bin/env bash
# Қате шықса тоқтату
set -o errexit

# Кітапханаларды орнату
pip install -r requirements.txt

# Базаны жаңарту (Migrate)
python manage.py migrate

# Статикалық файлдарды жинау
python manage.py collectstatic --no-input

# Админ жасау (Shell арқылы)
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'pass1234')
    print('Админ жасалды!')
else:
    print('Админ бұрыннан бар.')
END
