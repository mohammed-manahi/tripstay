from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from reservation.models import Reservation
from reservation.serializers import ReservationSerializer, CreateReservationSerializer, UpdateReservationSerializer
from reservation.permissions import CanAddOrUpdateReservation
from account.models import User


class ReservationViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    """
    Create view set for reservation model
    """
    # Define allowed http methods
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    permission_classes = [IsAuthenticated, CanAddOrUpdateReservation]

    # Use django-filter library to apply generic back-end filtering and search filter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Add search filter fields
    search_fields = ['reservation_from', 'reservation_to']


    def get_queryset(self):
        """
        Define reservation API query-set
        Where super user can view all orders and client can view only his/her own reservation
        :return:
        """
        return Reservation.objects.all()

    def get_serializer_class(self):
        """
        Define reservation api serializer
        :return:
        """
        # Define order API serializer
        if self.request.method == 'POST':
            return CreateReservationSerializer
        if self.request.method == 'PATCH':
            return UpdateReservationSerializer
        return ReservationSerializer

    def get_serializer_context(self):
        """
        Define reservation api context
        :return:
        """
        return {'request': self.request}
