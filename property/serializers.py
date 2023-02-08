from rest_framework import serializers
from property.models import Property, PropertyCategory, PropertyMedia, PropertyFeature, PropertyFeatureCategory, \
    PropertyReview


class PropertyCategorySerializer(serializers.ModelSerializer):
    """
    Create serializer for property category model
    """

    class Meta():
        model = PropertyCategory
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
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta():
        model = Property
        fields = ['name', 'description', 'slug', 'owner', 'category', 'address', 'location',
                  'number_of_bedrooms', 'number_of_beds', 'number_of_baths', 'capacity_for_adults',
                  'capacity_for_children', 'available', 'available_from', 'available_to']
