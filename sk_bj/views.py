from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True  # Админкаға кіруге рұқсат
            user.is_superuser = True  # Ең басты админ
            user.save()
            login(request, user)
            return redirect('/admin/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

import csv
import io
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Property, BankPayment

def upload_bank_file(request):
    if request.method == 'POST' and request.FILES.get('bank_file'):
        file = request.FILES['bank_file']
        decoded_file = file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        
        count = 0
        for row in reader:
            try:
                account = row['Лицевой счет']
                amount = float(row['Сумма'])
                payer = row['ФИО плательщика']
                
                prop = Property.objects.get(account_number=account)
                BankPayment.objects.get_or_create(
                    property=prop,
                    amount=amount,
                    payer_name=payer,
                    external_id=f"{account}_{amount}_{payer}"
                )
                count += 1
            except Exception as e:
                continue # Егер пәтер табылмаса, келесісіне көшеді
        
        messages.success(request, f"{count} төлем сәтті жүктелді!")
        return redirect('/admin/sk_bj/bankpayment/') # Төлемдер тізіміне қайтару
    
    return render(request, 'upload.html')

import json
import os
from django.conf import settings
from django.http import HttpResponse
from .models import Property

def import_json_data(request):
    json_path = os.path.join(settings.BASE_DIR, 'kz_tulem_database_2025-12-26.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    count = 0
    for apt in data['apartments']:
        Property.objects.update_or_create(
            apartment_id=apt['id'],
            defaults={
                'account_number': apt['account'],
                'address': f"{apt['id']}-пәтер",
                'area': apt['area'],
                'debt_maint': apt['initialDebt']['maint'],
                'debt_clean': apt['initialDebt']['clean'],
                'debt_sec': apt['initialDebt']['sec'],
                'debt_heat': apt['initialDebt']['heat'],
                'debt_cap': apt['initialDebt']['cap'],
            }
        )
        count += 1
    
    return HttpResponse(f"Сәтті аяқталды! {count} пәтер базаға жүктелді.")

import json
import os
from django.conf import settings
from django.http import HttpResponse
from .models import Property

def import_json_data(request):
    # Файлды жобаның негізгі папкасынан іздейміз
    json_path = os.path.join(settings.BASE_DIR, 'kz_tulem_database_2025-12-26.json')
    
    if not os.path.exists(json_path):
        return HttpResponse(f"Қате: {json_path} мекенжайында файл табылмады. GitHub-қа жүктегеніңізге көз жеткізіңіз.")

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    count = 0
    # JSON ішіндегі 'apartments' тізімін оқимыз
    for apt in data.get('apartments', []):
        Property.objects.update_or_create(
            apartment_id=apt['id'],
            defaults={
                'account_number': apt['account'],
                'area': apt['area'],
                'debt_maint': apt.get('initialDebt', {}).get('maint', 0),
                'debt_clean': apt.get('initialDebt', {}).get('clean', 0),
                'debt_sec': apt.get('initialDebt', {}).get('sec', 0),
                'debt_heat': apt.get('initialDebt', {}).get('heat', 0),
                'debt_cap': apt.get('initialDebt', {}).get('cap', 0),
            }
        )
        count += 1
    
    return HttpResponse(f"Сәтті аяқталды! {count} пәтер базаға жүктелді.")
