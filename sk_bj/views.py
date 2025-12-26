import json
import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Базаның жолы (Сіздің JSON файлыңыз)
DB_PATH = os.path.join(settings.BASE_DIR, 'kz_tulem_database_2025-12-26.json')

def get_db():
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

@csrf_exempt
def api_data_manager(request):
    """Админ панель үшін: деректерді алу және сақтау"""
    if request.method == 'POST':
        new_data = json.loads(request.body)
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
        return JsonResponse({'status': 'success'})
    
    # GET: Барлық базаны JSON ретінде қайтару
    return JsonResponse(get_db(), safe=False)

def pater_detail_view(request, apt_id):
    """Пайдаланушы үшін: Жеке бөлме (pater.html шаблоны)"""
    data = get_db()
    # Пәтерді ID бойынша іздеу (9 немесе 9а)
    apt = next((item for item in data if str(item['id']) == str(apt_id)), None)
    
    if apt:
        # Автоматты тариф: 1, 15, 16 - 60 тңг, қалғандары - 40 тңг
        apt['auto_rate'] = 60 if str(apt['id']) in ['1', '15', '16'] else 40
        return render(request, 'pater.html', {'apt': apt})
    
    return HttpResponse("Пәтер табылмады!", status=404)
