#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# Нұсқаулықтарды жасау және базаға енгізу
python manage.py makemigrations sk_bj
python manage.py migrate

# Егер create_admin.py файлыңыз болса, соны іске қосу
if [ -f create_admin.py ]; then
    python create_admin.py
fi
