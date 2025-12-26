from django.db import models

class Property(models.Model):
    # Пәтер нөмірі (мысалы, "9" немесе "9а")
    apartment_id = models.CharField(max_length=50, unique=True) 
    
    # Дербес шот (Каспи/Халық файлдарымен байланыстыру үшін)
    account_number = models.CharField(max_length=50, blank=True, null=True) 
    
    # --- ЖАҢА ӨРІС: Тұрғынның жеке кабинетіне кіру құпия сөзі ---
    # Әдепкі бойынша "12345" деп орнатамыз, кейін әркім өзі өзгерте алады
    password = models.CharField(max_length=100, default="12345")
    
    address = models.CharField(max_length=255, default="Мекенжай көрсетілмеген")
    area = models.FloatField(default=0.0)
    
    # Қарыздар бөлімі
    debt_maint = models.FloatField(default=0.0)
    debt_clean = models.FloatField(default=0.0)
    debt_sec = models.FloatField(default=0.0)
    debt_heat = models.FloatField(default=0.0)
    debt_cap = models.FloatField(default=0.0)

    # Жалпы қарызды есептейтін функция (Жеке кабинетте көрсету үшін ыңғайлы)
    def total_debt(self):
        return round(self.debt_maint + self.debt_clean + self.debt_sec + self.debt_heat + self.debt_cap, 2)

    def __str__(self):
        return f"Пәтер {self.apartment_id} (Шот: {self.account_number or 'Жоқ'})"

class BankPayment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payer_name = models.CharField(max_length=255)
    external_id = models.CharField(max_length=255, unique=True)

class Property(models.Model):
    # ... бұрынғы өрістер ...
    general_announcement = models.TextField(default="Төлемді уақытылы өтеуіңізді сұраймыз!", blank=True)
    private_note = models.TextField(null=True, blank=True)
