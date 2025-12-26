import json
import os
import csv
import io
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Модельдерді импорттау (Осы жерде қате болуы мүмкін)
from .models import Property, BankPayment 

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.is_superuser = True
            user.save()
            login(request, user)
            return redirect('/admin/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def import_json_data(request):
    json_path = os.path.join(settings.BASE_DIR, 'kz_tulem_database_2025-12-26.json')
    
    if not os.path.exists(json_path):
        return HttpResponse(f"Қате: {json_path} файлы табылмады.")

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
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
    except Exception as e:
        return HttpResponse(f"JSON қатесі: {str(e)}")

def upload_bank_file(request):
    if request.method == 'POST' and request.FILES.get('bank_file'):
        file = request.FILES['bank_file']
        decoded_file = file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        
        count = 0
        for row in reader:
            try:
                account = row.get('Лицевой счет')
                amount = float(row.get('Сумма', 0))
                payer = row.get('ФИО плательщика', '')
                
                prop = Property.objects.get(account_number=account)
                BankPayment.objects.create(
                    property=prop,
                    amount=amount,
                    payer_name=payer,
                    external_id=f"{account}_{amount}_{payer}"
                )
                count += 1
            except:
                continue
        
        messages.success(request, f"{count} төлем сәтті жүктелді!")
        return redirect('/admin/sk_bj/bankpayment/')
    
    return render(request, 'upload.html')
