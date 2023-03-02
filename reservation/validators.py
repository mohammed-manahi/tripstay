from django.core.exceptions import ValidationError
import property.models
from reservation.models import Reservation


def validate_reservation_start_date():
    if not Reservation.reservation_from <= property.models.Property.available_from:
        raise ValidationError('Reservation must occur when the property is available')


def validate_reservation_end_date():
    if not Reservation.reservation_to <= property.models.Property.available_to:
        raise ValidationError('Reservation must occur when the property is available')
