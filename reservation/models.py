from django.db import models
from property.models import Property
from django.conf import settings



class Reservation(models.Model):
    """
    Create property reservation model and associate it with property and user models
    """
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='reservation')
    reservation_from = models.DateTimeField()
    reservation_to = models.DateTimeField()
    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservation')
    reserved = models.BooleanField(default=False)

    class Meta():
        # Define meta attributes
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def __str__(self):
        return f'{self.guest} reservation'
