from django.db.models.aggregates import Avg
from rest_framework import serializers
from property.models import Property, Category, Media, Feature, FeatureCategory, Review


class MediaSerializer(serializers.ModelSerializer):
    """
    Create serializer for media model
    """

    class Meta():
        model = Media
        fields = ['id', 'name', 'description', 'photo', 'video']

    def create(self, validated_data):
        """
        Override create method to allow nested route for media in property api endpoint
        :param validated_data:
        :return:
        """
        property_id = self.context['property_id']
        return Media.objects.create(property_id=property_id, **validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    """
    Create serializer for review model
    """
    # Get current authenticated user
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta():
        model = Review
        fields = ['id', 'comment', 'rate', 'user']

    def validate(self, attrs):
        property_id = self.context['property_id']
        user = attrs['user']
        if Review.objects.filter(property_id=property_id, user=user).exists():
            raise serializers.ValidationError('You have already reviewed this property')
        return attrs

    def create(self, validated_data):
        """
        Override create method to allow nested route for media in property api endpoint
        :param validated_data:
        :return:
        """
        property_id = self.context['property_id']
        return Review.objects.create(property_id=property_id, **validated_data)


class CategorySerializer(serializers.ModelSerializer):
    """
    Create serializer for category model
    """

    class Meta():
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'property_count']

    # Custom field that calls get property category method
    property_count = serializers.SerializerMethodField(method_name='get_property_count')

    def get_property_count(self, property_category):
        # Custom method to get number of properties in a category
        return property_category.properties.count()


class PropertySerializer(serializers.ModelSerializer):
    """
    Create serializer for property model
    """
    # Get current authenticated user
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
        fields = ['id', 'name', 'description', 'slug', 'owner', 'category', 'address', 'location',
                  'number_of_bedrooms', 'number_of_beds', 'number_of_baths', 'capacity_for_adults',
                  'capacity_for_children', 'price_per_night', 'available', 'available_from', 'available_to',
                  'average_rate', 'media', 'reviews']

    # Display property media
    media = MediaSerializer(many=True, read_only=True)

    # Display property reviews
    reviews = ReviewSerializer(many=True, read_only=True)

    # Custom field for average review rate
    average_rate = serializers.SerializerMethodField(method_name='get_average_rate')

    def get_average_rate(self, property):
        return property.reviews.all().aggregate(Avg('rate'))


class FeatureCategorySerializer(serializers.ModelSerializer):
    """
    Create serializer for feature category model
    """

    class Meta():
        model = FeatureCategory
        fields = ['name', 'description', 'slug']
