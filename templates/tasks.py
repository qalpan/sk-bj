# Логиканың қарапайым көрінісі
def monthly_billing():
    for apartment in Apartments.objects.all():
        # Жаңа айға есептеу
        new_charge = (apartment.area * 40) + 850 + 300 + (apartment.area * 5) + (apartment.area * 40)
        # Қарызды жаңарту
        apartment.balance += new_charge
        apartment.save()
