import json
import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# База файлының жолы
DB_PATH = os.path.join(settings.BASE_DIR, 'kz_tulem_database_2025-12-26.json')

@csrf_exempt
def api_manager(request, apt_id=None):
    # 1. Базаны оқу
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return HttpResponse("База файлы табылмады!", status=500)

    # 2. АДМИН ПАНЕЛЬ ҮШІН (POST - Сақтау)
    if request.method == 'POST':
        try:
            updated_data = json.loads(request.body)
            with open(DB_PATH, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=4)
            return JsonResponse({'status': 'success', 'message': 'Деректер сақталды'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # 3. ПАЙДАЛАНУШЫ ҮШІН (Түбіртек - HTML)
    if apt_id:
        # Пәтерді ID бойынша іздеу (мысалы: 9 немесе 9а)
        apt = next((item for item in data if str(item['id']) == str(apt_id)), None)
        if apt:
            # Авто-тариф логикасы: 1, 15, 16 пәтерлер - 60, қалғандары - 40
            apt['auto_rate'] = 60 if str(apt['id']) in ['1', '15', '16'] else 40
            return render(request, 'pater.html', {'apt': apt})
        return HttpResponse("Пәтер табылмады!", status=404)

    # 4. АДМИН ПАНЕЛЬ ҮШІН (GET - Барлық базаны алу)
    return JsonResponse(data, safe=False)
