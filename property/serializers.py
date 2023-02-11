from rest_framework import serializers
from property.models import Property, Category, Media, Feature, FeatureCategory, Review


class PropertyCategorySerializer(serializers.ModelSerializer):
    """
    Create serializer for property category model
    """

    class Meta():
        model = Category
        fields = ['name', 'description', 'slug', 'property_count']

    # Custom field that calls get property category method
    property_count = serializers.SerializerMethodField(method_name='get_property_count')

    def get_property_count(self, property_category):
        # Custom method to get number of properties in a category
        return property_category.properties.count()


class PropertySerializer(serializers.ModelSerializer):
    """
    Create serializer for property model
    """
    # Get current user as a hidden field
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, attrs):
        """
        Custom validation for available from and available to fields
        :param attrs:
        :return:
        """
        if attrs['available_from'] > attrs['available_to']:
            raise serializers.ValidationError('Available to date must occur after available from date')
        return attrs

    class Meta():
        model = Property
        fields = ['name', 'description', 'slug', 'owner', 'category', 'address', 'location',
                  'number_of_bedrooms', 'number_of_beds', 'number_of_baths', 'capacity_for_adults',
                  'capacity_for_children', 'price_per_night', 'available', 'available_from', 'available_to']
