import json
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# 1. Жобаның негізгі папкасын (root) анықтаймыз
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Сіздің жүктеген базаңыздың нақты аты
DB_NAME = 'kz_tulem_database_2025-12-26.json'

# 3. Файлды екі жерден іздейміз: негізгі папкадан немесе sk_bj ішінен
DATA_FILE = os.path.join(BASE_DIR, DB_NAME)
if not os.path.exists(DATA_FILE):
    DATA_FILE = os.path.join(BASE_DIR, 'sk_bj', DB_NAME)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"apartments": []}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"apartments": []}

@csrf_exempt
def api_manager(request, apt_id=None):
    try:
        if request.method == 'GET':
            # Егер URL-де pater нөмірі болса, HTML көрсету
            if apt_id or 'pater' in request.path:
                return render(request, 'pater.html', {'apt_id': apt_id})
            
            # API деректерін JSON түрінде беру
            data = load_data()
            return JsonResponse(data, safe=False)

        if request.method == 'POST':
            new_data = json.loads(request.body)
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
            return JsonResponse({"status": "ok"})
            
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def admin_panel(request):
    return render(request, 'tөlemesep_smart.html')
