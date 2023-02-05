from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from property.models import Property, PropertyCategory, PropertyMedia, PropertyFeature, PropertyFeatureCategory, \
    PropertyReview
from property.serializers import PropertySerializer
from property.permissions import CanAddOrUpdateProperty


class PropertyViewSet(ModelViewSet):
    """
    Create view set for property model
    """
    # Use django-filter library to apply generic back-end filtering and search filter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Add search filter fields
    search_fields = ['name', 'description']

    # Add sorting filter fields
    ordering_fields = ['perice_per_night', 'updated_at']

    # Set custom permission class
    permission_classes = [IsAuthenticated, CanAddOrUpdateProperty]

    def get_queryset(self):
        # Define property API query-set
        return Property.objects.all()

    def get_serializer_class(self):
        # Define property API serializer
        return PropertySerializer

    def get_serializer_context(self):
        # Define property API context
        return {"request": self.request}
