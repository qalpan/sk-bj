import json
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# JSON файлының жолы
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Файлдың нақты орнын тексеріңіз: ол 'sk_bj' папкасының ішінде болуы керек
DATA_FILE = os.path.join(BASE_DIR, 'sk_bj', 'apartments.json')

def load_data():
    if not os.path.exists(DATA_FILE):
        # Егер файл жоқ болса, бос құрылым қайтару
        return {"apartments": []}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"apartments": []}

@csrf_exempt
def api_manager(request, apt_id=None):
    try:
        if request.method == 'GET':
            # Егер URL-де пәтер нөмірі болса (мысалы, /pater/1/), HTML бетті ашу
            if 'pater' in request.path:
                return render(request, 'pater.html', {'apt_id': apt_id})
            
            # Әйтпесе JSON деректерін қайтару
            data = load_data()
            return JsonResponse(data, safe=False)

        if request.method == 'POST':
            new_data = json.loads(request.body)
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
            return JsonResponse({"status": "ok"})
            
    except Exception as e:
        # Қате болса, оны JSON түрінде қайтару (дизайн бұзылмауы үшін)
        return JsonResponse({"error": str(e)}, status=500)

def admin_panel(request):
    return render(request, 'tөlemesep_smart.html')
