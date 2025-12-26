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
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for apt in data.get('apartments', []):
            # Тек қана apartment_id бойынша іздейміз
            Property.objects.update_or_create(
                apartment_id=str(apt['id']), # Мысалы: "9", "9а"
                defaults={
                    'account_number': apt.get('account'), # Қайталанса да қабылдайды
                    'area': apt.get('area', 0),
                    'debt_maint': apt.get('initialDebt', {}).get('maint', 0),
                    'debt_clean': apt.get('initialDebt', {}).get('clean', 0),
                    'debt_sec': apt.get('initialDebt', {}).get('sec', 0),
                    'debt_heat': apt.get('initialDebt', {}).get('heat', 0),
                    'debt_cap': apt.get('initialDebt', {}).get('cap', 0),
                }
            )
            count += 1
        return HttpResponse(f"Сәтті аяқталды! {count} пәтер өңделді.")
    except Exception as e:
        return HttpResponse(f"Қате шықты: {str(e)}")

def upload_bank_file(request):
    if request.method == 'POST' and request.FILES.get('bank_file'):
        file = request.FILES['bank_file']
        decoded_file = file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        
        # Бірінші жол баған атаулары емес болса, оны өткізіп жіберу үшін:
        lines = io_string.readlines()
        if len(lines) > 0 and 'РЕЕСТР' in lines[0]:
            io_string = io.StringIO("".join(lines[1:]))
        else:
            io_string = io.StringIO("".join(lines))

        reader = csv.DictReader(io_string)
        count = 0
        
        for row in reader:
            try:
                # Баған аттарын бірнеше нұсқада іздейміз (Kaspi және Halyk үшін)
                account = row.get('Лицевой номер') or row.get('Лицевой счет')
                amount = row.get('Сумма')
                payer = row.get('ФИО') or row.get('ФИО плательщика')
                
                if not account or not amount:
                    continue

                # Пәтерді базадан іздеу
                prop = Property.objects.get(account_number=account.strip())
                
                # Төлемді жазу
                BankPayment.objects.get_or_create(
                    property=prop,
                    amount=float(amount),
                    payer_name=payer or "Белгісіз",
                    external_id=f"{account}_{amount}_{payer}"
                )
                count += 1
            except Exception as e:
                print(f"Қате: {e}")
                continue
        
        messages.success(request, f"{count} төлем сәтті жүктелді!")
        return redirect('/admin/sk_bj/bankpayment/')
    
    return render(request, 'upload.html')
