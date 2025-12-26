import json
import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# База файлының жолы (root-та тұрған JSON)
DB_PATH = os.path.join(settings.BASE_DIR, 'kz_tulem_database_2025-12-26.json')

@csrf_exempt
def api_manager(request, apt_id=None):
    # Базаны оқу
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return HttpResponse("База файлы табылмады!", status=500)

    # АДМИН ПАНЕЛЬ: Деректерді сақтау (POST)
    if request.method == 'POST':
        updated_data = json.loads(request.body)
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=4)
        return JsonResponse({'status': 'success'})

    # ПАЙДАЛАНУШЫ: Жеке түбіртегі (HTML)
    if apt_id:
        apt = next((item for item in data if str(item['id']) == str(apt_id)), None)
        if apt:
            # Авто-тариф: 1, 15, 16 - 60 тңг, басқалары - 40 тңг
            apt['auto_rate'] = 60 if str(apt['id']) in ['1', '15', '16'] else 40
            return render(request, 'pater.html', {'apt': apt})
        return HttpResponse("Пәтер табылмады!", status=404)

    # АДМИН ПАНЕЛЬ: Деректерді алу (GET)
    return JsonResponse(data, safe=False)

def resident_auth(request):
    return HttpResponse("Логин беті әлі дайын емес")
