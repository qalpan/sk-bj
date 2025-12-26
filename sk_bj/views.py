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
        # Файлды оқу
        try:
            decoded_file = file.read().decode('utf-8-sig') # utf-8-sig Excel файлдарындағы қателерді түзетеді
        except UnicodeDecodeError:
            decoded_file = file.read().decode('cp1251') # Егер utf-8 болмаса, қазақша шрифттерді осылай оқимыз
            
        io_string = io.StringIO(decoded_file)
        lines = io_string.readlines()

        # Егер бұл Kaspi-дің реестрі болса (бірінші жолын өткізіп жібереміз)
        if len(lines) > 0 and ("РЕЕСТР" in lines[0] or "системе электронного" in lines[0]):
            csv_data = "".join(lines[1:])
        else:
            csv_data = "".join(lines)

        reader = csv.DictReader(io_string)
        io_string = io.StringIO(csv_data)
        reader = csv.DictReader(io_string)
        
        count = 0
        for row in reader:
            # Әртүрлі банктердің баған атауларын тексеру
            account = row.get('Лицевой номер') or row.get('Лицевой счет')
            amount_raw = row.get('Сумма')
            payer = row.get('ФИО') or row.get('ФИО плательщика')
            
            # Егер жол бос болса немесе "Общая сумма" деген сияқты қорытынды жол болса өткізіп жібереміз
            if not account or not amount_raw or "Общая" in str(account):
                continue

            try:
                # Мәтінді санға айналдыру
                amount = float(str(amount_raw).replace(',', '.'))
                
                # Базадан пәтерді іздеу
                prop = Property.objects.get(account_number=account.strip())
                
                # Төлемді базаға қосу
                BankPayment.objects.get_or_create(
                    property=prop,
                    amount=amount,
                    payer_name=payer.strip() if payer else "Белгісіз",
                    external_id=f"{account.strip()}_{amount}_{payer}_{row.get('Дата', '')}"
                )
                count += 1
            except Property.DoesNotExist:
                print(f"Пәтер табылмады: {account}")
                continue
            except Exception as e:
                print(f"Жолды өңдеуде қате: {e}")
                continue
        
        messages.success(request, f"{count} төлем сәтті өңделді!")
        return redirect('/admin/sk_bj/bankpayment/')
    
    return render(request, 'upload.html')

def resident_cabinet(request):
    if request.method == 'POST':
        apt_id = request.POST.get('apt_id')
        pwd = request.POST.get('password')
        try:
            property_obj = Property.objects.get(apartment_id=apt_id, password=pwd)
            return render(request, 'cabinet.html', {'property': property_obj})
        except Property.DoesNotExist:
            return render(request, 'login.html', {'error': 'Пәтер нөмірі немесе құпия сөз қате!'})
    return render(request, 'login.html')

def resident_auth(request):
    if request.method == 'POST':
        apt_id = request.POST.get('apt_id')
        pwd = request.POST.get('password')
        action = request.POST.get('action') # 'login' немесе 'signup'

        try:
            prop = Property.objects.get(apartment_id=apt_id)
            
            if action == 'signup':
                # Егер пароль әлі "12345" (бастапқы) болса, жаңасын орнатады
                prop.password = pwd
                prop.save()
                return render(request, 'cabinet.html', {'property': prop})
            
            elif action == 'login':
                if prop.password == pwd:
                    return render(request, 'cabinet.html', {'property': prop})
                else:
                    return render(request, 'login.html', {'error': 'Құпия сөз қате!'})
                    
        except Property.DoesNotExist:
            return render(request, 'login.html', {'error': 'Мұндай пәтер базада жоқ!'})
    
    return render(request, 'login.html')
