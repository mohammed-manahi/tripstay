from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from property.models import Property, Category, Media, Feature, FeatureCategory, Review
from property.serializers import PropertySerializer, CategorySerializer, MediaSerializer
from property.permissions import CanAddOrUpdateProperty, AdminOnlyActions


class PropertyViewSet(ModelViewSet):
    """
    Create view set for property model
    """
    # Use django-filter library to apply generic back-end filtering and search filter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Add search filter fields
    search_fields = ['name', 'description']

    # Add sorting filter fields
    ordering_fields = ['name', 'price_per_night']

    # Set custom permission class
    permission_classes = [IsAuthenticated, CanAddOrUpdateProperty]

    def get_queryset(self):
        """
        Define property api query-set
        :return:
        """
        return Property.objects.select_related('category').prefetch_related('media').all()

    def get_serializer_class(self):
        """
        Define property api serializer
        :return:
        """
        return PropertySerializer

    def get_serializer_context(self):
        """
        Define property api context
        :return:
        """
        return {'request': self.request}


class CategoryViewSet(ModelViewSet):
    """
    Create view set for category model
    """
    # Use django-filter library to apply generic back-end filtering and search filter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Add search filter fields
    search_fields = ['name', 'description']

    # Add sorting filter fields
    ordering_fields = ['name']

    # Set custom permission class
    permission_classes = [IsAuthenticated, AdminOnlyActions]

    def get_queryset(self):
        """
        Define category api query-set
        :return:
        """
        return Category.objects.prefetch_related('properties').all()

    def get_serializer_class(self):
        """
        Define category api serializer
        :return:
        """
        return CategorySerializer

    def get_serializer_context(self):
        """
        Define property api context
        :return:
        """
        return {'request': self.request}


class MediaViewSet(ModelViewSet):
    """
    Create media view set for media model
    """
    # Set custom permission class
    permission_classes = [IsAuthenticated, CanAddOrUpdateProperty]

    def get_queryset(self):
        """
        Define media api queryset
        :return:
        """
        return Media.objects.filter(property_id=self.kwargs.get('property_pk'))

    def get_serializer_class(self):
        """
         Define media api serializer
        :return:
        """
        return MediaSerializer

    def get_serializer_context(self):
        """
        Define media api context
        :return:
        """
        return {'request': self.request, 'property_id': self.kwargs.get('property_pk')}
