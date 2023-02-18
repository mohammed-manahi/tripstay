from django.contrib import admin
from reservation.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['property', 'reservation_from', 'reservation_to', 'reservation_to', 'guest']
    list_filter = ['guest', 'property']
