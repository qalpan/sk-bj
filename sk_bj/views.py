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

from django.shortcuts import render, redirect
from .models import Property

def resident_auth(request):
    if request.method == 'POST':
        # strip() — бос орындарды алып тастайды, lower() — кіші әріпке айналдырады
        apt_id = request.POST.get('apt_id', '').strip().lower()
        pwd = request.POST.get('password')
        action = request.POST.get('action')

        try:
            # Базадан іздегенде де кіші әріппен және дәл сәйкестікпен іздейміз
            # Ескерту: Базадағы apartment_id-лерді де кіші әріпке келтіру керек болуы мүмкін
            prop = Property.objects.filter(apartment_id__iexact=apt_id).first()
            
            if not prop:
                return render(request, 'login.html', {'error': f'"{apt_id}" пәтері базада табылмады!'})

            if action == 'signup':
                prop.password = pwd
                prop.save()
                return render(request, 'cabinet.html', {'property': prop})
            
            elif action == 'login':
                if prop.password == pwd:
                    return render(request, 'cabinet.html', {'property': prop})
                else:
                    return render(request, 'login.html', {'error': 'Құпия сөз қате!'})
        
        except Exception as e:
            return render(request, 'login.html', {'error': f'Жүйелік қате: {str(e)}'})

    return render(request, 'login.html')

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def import_from_json(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            apartments_list = data.get('apartments', data)
            
            for item in apartments_list:
                # 1. Ең соңғы айдағы қарызды (ledger) алуға тырысамыз
                ledger = item.get('ledger', [])
                if ledger and len(ledger) > 0:
                    # Ең соңғы айды аламыз (мысалы, Желтоқсан)
                    last_month_data = ledger[-1].get('accumulated', {})
                    maint = last_month_data.get('maint', 0)
                    clean = last_month_data.get('clean', 0)
                    sec = last_month_data.get('sec', 0)
                    heat = last_month_data.get('heat', 0)
                    cap = last_month_data.get('cap', 0)
                else:
                    # Егер ledger бос болса, initialDebt-ті аламыз
                    debts = item.get('initialDebt', item.get('debt', {}))
                    maint = debts.get('maint', 0)
                    clean = debts.get('clean', 0)
                    sec = debts.get('sec', 0)
                    heat = debts.get('heat', 0)
                    cap = debts.get('cap', 0)

                # 2. Базаны жаңарту
                Property.objects.update_or_create(
                    apartment_id=str(item.get('id')),
                    defaults={
                        'account_number': item.get('account'),
                        'area': item.get('area', 0.0),
                        'debt_maint': maint,
                        'debt_clean': clean,
                        'debt_sec': sec,
                        'debt_heat': heat,
                        'debt_cap': cap,
                    }
                )
            return JsonResponse({'status': 'success', 'message': f'{len(apartments_list)} пәтердің соңғы есептері жүктелді'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return render(request, 'import_page.html')

def generate_receipt(request, apt_id):
    prop = Property.objects.get(apartment_id=apt_id)
    
    # Төлем сілтемелерін дайындау (мысалы)
    kaspi_url = f"https://kaspi.kz/pay/OSI_AKSAI_3_10A?service=1&apt={apt_id}"
    halyk_url = f"https://homebank.kz/payments/common/OSI_AKSAI?apt={apt_id}"

    context = {
        'prop': prop,
        'kaspi_url': kaspi_url,
        'halyk_url': halyk_url,
        'current_month': "Желтоқсан / Декабрь 2025"
    }
    return render(request, 'receipt_template.html', context)

def generate_receipt(request):
    # Пайдаланушы қай пәтермен кірсе, соның дерегін аламыз
    apt_id = request.session.get('apt_id') 
    if not apt_id:
        return redirect('login')
        
    prop = Property.objects.get(apartment_id=apt_id)
    
    # Kaspi және Halyk сілтемелері (пәтер нөмірімен бірге)
    kaspi_url = f"https://kaspi.kz/pay/OSI_AKSAI_3_10A?service=1&apt={prop.apartment_id}"
    halyk_url = f"https://homebank.kz/payments/common/OSI_AKSAI?apt={prop.apartment_id}"

    context = {
        'prop': prop,
        'kaspi_url': kaspi_url,
        'halyk_url': halyk_url,
        'month': "Желтоқсан / Декабрь 2025"
    }
    return render(request, 'receipt.html', context)
