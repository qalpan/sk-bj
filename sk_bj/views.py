import json
import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Файл жолын анықтаудың ең сенімді жолы:
# Бұл views.py файлы тұрған папканы (sk_bj) табады
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(CURRENT_DIR, 'apartments.json')

def load_data():
    if not os.path.exists(DATA_FILE):
        # Егер файл жоқ болса, бос тізім қайтарамыз
        return {"apartments": []}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"apartments": []}

@csrf_exempt
def api_manager(request, apt_id=None):
    try:
        if request.method == 'GET':
            # Пәтер бетін ашу
            if apt_id or 'pater' in request.path:
                return render(request, 'pater.html', {'apt_id': apt_id})
            
            # API деректерін қайтару
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
