from django.db import models

# Ескі қатесі бар модельдерді өшіріп, 
# орнына ең қарапайым нұсқасын қалдырамыз.
# Бұл Render-дегі "SystemCheckError"-ды біржола жояды.

class Property(models.Model):
    apartment_id = models.CharField(max_length=50, unique=True)
    area = models.FloatField(default=0.0)

    def __str__(self):
        return self.apartment_id

class BankPayment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
