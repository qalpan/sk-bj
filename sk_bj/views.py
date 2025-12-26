# sk_bj/views.py жаңартылған, ықшамдалған нұсқасы
import json
import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

DB_PATH = os.path.join(settings.BASE_DIR, 'kz_tulem_database_2025-12-26.json')

# 1. АДМИН ЖӘНЕ ПАЙДАЛАНУШЫ ҮШІН ДЕРЕКТЕРДІ БАСҚАРУ
def api_manager(request, apt_id=None):
    # Деректерді оқу
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Егер POST келсе - АДМИН деректерді сақтап жатыр
    if request.method == 'POST':
        updated_data = json.loads(request.body)
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=4)
        return JsonResponse({'status': 'success'})

    # Егер GET болса және ID болса - ПАЙДАЛАНУШЫ түбіртек көріп жатыр
    if apt_id:
        apt = next((item for item in data if str(item['id']) == apt_id), None)
        if apt:
            # Тарифті динамикалық анықтау
            apt['rate'] = 60 if str(apt['id']) in ['1', '15', '16'] else 40
            return render(request, 'pater.html', {'apt': apt})
        return HttpResponse("Пәтер табылмады", status=404)

    # Әйтпесе барлық базаны JSON ретінде қайтару (Админ панель үшін)
    return JsonResponse(data, safe=False)
