from django.db import models
from django.contrib.auth.models import User

class Tariff(models.Model):
    name = models.CharField(max_length=100) # Мысалы: Aqsai3-10a
    price = models.DecimalField(max_digits=10, decimal_places=2) # 40тг

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    area = models.DecimalField(max_digits=10, decimal_places=2)
    build_year = models.IntegerField()
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True)
