import json
import os
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# JSON файлының жолы
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, 'sk_bj', 'apartments.json')

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

@csrf_exempt
def api_manager(request, apt_id=None):
    if request.method == 'GET':
        data = load_data()
        # Егер /pater/1/ деп ашылса, HTML бетті көрсетеміз
        if apt_id:
            return render(request, 'pater.html', {'apt_id': apt_id})
        # Әйтпесе JSON деректі береміз
        return JsonResponse(data, safe=False)
    
    if request.method == 'POST':
        new_data = json.loads(request.body)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
        return JsonResponse({"status": "ok"})
