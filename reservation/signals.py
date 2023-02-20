from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from reservation.models import Reservation


@receiver(post_save, sender=Reservation)
def update_reservation_status_on_create(sender, instance, created, **kwargs):
    """
    Update reservation status on create
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        Reservation.objects.update(reserved=True)


