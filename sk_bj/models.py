from django.db import models

class Tariff(models.Model):
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_per_sqm = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Property(models.Model):
    address = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.address} ({self.owner_name})"

class Invoice(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    month = models.DateField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, editable=False)

    def save(self, *args, **kwargs):
        total = 0
        tariffs = Tariff.objects.all()
        for t in tariffs:
            if t.is_per_sqm:
                total += t.rate * self.property.area
            else:
                total += t.rate
        self.total_amount = total
        super().save(*args, **kwargs)
        
class Payment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    bank_reference = models.CharField(max_length=255, unique=True) # Банктегі транзакция нөмірі (қайталанбау үшін)

from django.db import models

class Property(models.Model):
    address = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    # ЖАҢА: Дербес шотты сақтау үшін
    account_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.address} ({self.account_number})"

# ЖАҢА: Банк төлемдерін сақтау үшін
class BankPayment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='payments')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payer_name = models.CharField(max_length=255)
    external_id = models.CharField(max_length=100, unique=True) 

    def __str__(self):
        return f"{self.amount} тг - {self.payer_name}"
    def __str__(self):
        return f"{self.property.account_number}: {self.amount} тг"

class Property(models.Model):
    account_number = models.CharField("Дербес шот", max_length=20, unique=True)
    address = models.CharField("Пәтер нөмірі", max_length=50)
    area = models.DecimalField("Аудан", max_digits=10, decimal_places=2)
    
    # Бастапқы қалдықтар (Жыл басындағы қарыз)
    initial_maint_debt = models.DecimalField("ПИК қарызы", max_digits=15, decimal_places=2, default=0)
    initial_cap_debt = models.DecimalField("Күрделі жөндеу қарызы", max_digits=15, decimal_places=2, default=0)
    # ... басқа да қарыз түрлері
