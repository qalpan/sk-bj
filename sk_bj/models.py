from django.db import models

class Property(models.Model):
    apartment_id = models.CharField(max_length=50, unique=True)
    account_number = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=255, default="Мекенжай көрсетілмеген") # ОСЫ ЖОЛДЫ ҚОСЫҢЫЗ
    area = models.FloatField(default=0.0)
    debt_maint = models.FloatField(default=0.0)
    debt_clean = models.FloatField(default=0.0)
    debt_sec = models.FloatField(default=0.0)
    debt_heat = models.FloatField(default=0.0)
    debt_cap = models.FloatField(default=0.0)

    def __str__(self):
        return f"Пәтер {self.apartment_id}"

class BankPayment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payer_name = models.CharField(max_length=255)
    external_id = models.CharField(max_length=255, unique=True)
