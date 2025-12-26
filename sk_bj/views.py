import json
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Файлды іздейтін нақты папка
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# СІЗДІҢ ФАЙЛЫҢЫЗДЫҢ НАТҚЫ АТЫ:
DB_NAME = 'kz_tulem_database_2025-12-26.json'
DATA_FILE = os.path.join(CURRENT_DIR, DB_NAME)

def load_data():
    # Файл бар ма, жоқ па екенін тексеру (Консольге шығару)
    if not os.path.exists(DATA_FILE):
        print(f"ҚАТЕ: {DATA_FILE} файлы табылмады!")
        return {"apartments": []}
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"JSON ОҚУ ҚАТЕСІ: {e}")
        return {"apartments": []}

@csrf_exempt
def api_manager(request, apt_id=None):
    try:
        # Егер пәтер бетіне (pater/1/) кірсе
        if 'pater' in request.path:
            return render(request, 'pater.html', {'apt_id': apt_id})
        
        # API деректерін алу
        if request.method == 'GET':
            data = load_data()
            return JsonResponse(data, safe=False)

        # Деректерді сақтау
        if request.method == 'POST':
            new_data = json.loads(request.body)
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
            return JsonResponse({"status": "ok"})
            
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def admin_panel(request):
    return render(request, 'tөlemesep_smart.html')
