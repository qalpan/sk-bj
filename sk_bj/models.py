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
