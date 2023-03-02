from _decimal import Decimal
from rest_framework import serializers
from reservation.models import Reservation
from property.models import Property
from property.serializers import PropertySerializer


class ReservationSerializer(serializers.ModelSerializer):
    """
    Create serializer for reservation model
    """

    # Get guest user using the relation between reservation model and user model
    guest = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # Get property form property serializer
    property = PropertySerializer()

    class Meta():
        model = Reservation
        fields = ['id', 'guest', 'property', 'reservation_from', 'reservation_to', 'reserved',
                  'reservation_in_nights', 'reservation_fees', 'total_fees']

    # Custom field for reservation duration in days
    reservation_in_nights = serializers.SerializerMethodField(method_name='get_reservation_in_nights')

    # Custom field for reservation fee calculation
    reservation_fees = serializers.SerializerMethodField(method_name='calculate_reservation_fees')

    # Custom field for total fees
    total_fees = serializers.SerializerMethodField(method_name='calculate_total_fees')

    def get_reservation_in_nights(self, reservation):
        start_date = reservation.reservation_from
        end_date = reservation.reservation_to
        return abs((end_date - start_date).days)

    def calculate_reservation_fees(self, reservation):
        reservation_fees = reservation.property.price_per_night * self.get_reservation_in_nights(reservation)
        return reservation_fees

    def calculate_total_fees(self, reservation):
        service_fees = (Decimal(0.12) * self.calculate_reservation_fees(reservation))
        return service_fees + self.calculate_reservation_fees(reservation)


class CreateReservationSerializer(serializers.ModelSerializer):
    """
    Custom serializer for create action of reservation
    """
    # Get current authenticated user
    guest = serializers.HiddenField(default=serializers.CurrentUserDefault())
    property_id = serializers.IntegerField()
    reserved = serializers.HiddenField(default=False)

    def validate_property_id(self, property_id):
        """
        Validate property exists
        :param property_id:
        :return:
        """
        if not Property.objects.filter(id=property_id).exists():
            raise serializers.ValidationError("No property with given id not found")
        return property_id

    def validate(self, attrs):
        """
        Custom validation for available from and available to fields
        :param attrs:
        :return:
        """
        if attrs['reservation_from'] > attrs['reservation_to']:
            raise serializers.ValidationError('Available to date must occur after available from date')
        if Reservation.objects.filter(property_id=attrs['property_id'], reserved=True).exists():
            raise serializers.ValidationError('This property is currently reserved')
        return attrs

    class Meta():
        model = Reservation
        fields = ['id', 'guest', 'property_id', 'reservation_from', 'reservation_to', 'reserved']


class UpdateReservationSerializer(serializers.ModelSerializer):
    """
     Custom serializer for update action of reservation
     """

    class Meta():
        model = Reservation
        fields = ['reservation_from', 'reservation_to']
