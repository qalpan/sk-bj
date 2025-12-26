from django.db import models

class Property(models.Model):
    apartment_id = models.CharField("ID", max_length=10, unique=True)
    account_number = models.CharField("Дербес шот", max_length=20, unique=True)
    address = models.CharField("Пәтер нөмірі", max_length=50)
    area = models.DecimalField("Аудан (м2)", max_digits=10, decimal_places=2)
    owner_name = models.CharField("Иесі", max_length=100, blank=True, null=True)
    
    # Жыл басындағы қарыздар (initialDebt)
    debt_maint = models.DecimalField("ПИК қарызы", max_digits=15, decimal_places=2, default=0)
    debt_clean = models.DecimalField("Тазалық қарызы", max_digits=15, decimal_places=2, default=0)
    debt_sec = models.DecimalField("Бейнебақылау қарызы", max_digits=15, decimal_places=2, default=0)
    debt_heat = models.DecimalField("Жылу есептегіш қарызы", max_digits=15, decimal_places=2, default=0)
    debt_cap = models.DecimalField("Күрделі жөндеу қарызы", max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.address} ({self.account_number})"

class BankPayment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='payments')
    date = models.DateTimeField("Төлем күні", auto_now_add=True)
    amount = models.DecimalField("Сома", max_digits=15, decimal_places=2)
    payer_name = models.CharField("Төлеуші", max_length=255)
    external_id = models.CharField("Транзакция ID", max_length=100, unique=True)

    def __str__(self):
        return f"{self.amount} тг - {self.payer_name}"
