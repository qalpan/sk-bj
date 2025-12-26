from django.db import models

class Property(models.Model):
    # Пәтер нөмірі (мысалы, "9" немесе "9а") әрқашан бірегей (unique) болуы тиіс
    apartment_id = models.CharField(max_length=50, unique=True) 
    
    # Дербес шот енді қайталана береді немесе бос бола алады
    account_number = models.CharField(max_length=50, blank=True, null=True) 
    
    address = models.CharField(max_length=255, default="Мекенжай көрсетілмеген")
    area = models.FloatField(default=0.0)
    debt_maint = models.FloatField(default=0.0)
    debt_clean = models.FloatField(default=0.0)
    debt_sec = models.FloatField(default=0.0)
    debt_heat = models.FloatField(default=0.0)
    debt_cap = models.FloatField(default=0.0)

    def __str__(self):
        return f"Пәтер {self.apartment_id} (Шот: {self.account_number or 'Жоқ'})"

class BankPayment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payer_name = models.CharField(max_length=255)
    external_id = models.CharField(max_length=255, unique=True)
