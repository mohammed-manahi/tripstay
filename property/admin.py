from django.contrib import admin
from property.models import Property, PropertyMedia, PropertyFeature, PropertyFeatureCategory, PropertyReview, \
    PropertyCategory


@admin.register(PropertyMedia)
class PropertyMedia(admin.ModelAdmin):
    """
    Add property media model as inline view for property model in admin site
    """
    list_display = ['name', 'property']
    list_filter = ['property']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """
    Register property model in admin site
    """
    list_display = ['name', 'description', 'host_user', 'guest_user', 'address', 'available', 'price_per_night',
                    'cancellation_policy']
    list_filter = ['category', 'available', 'cancellation_policy']


@admin.register(PropertyFeatureCategory)
class PropertyFeatureCategoryAdmin(admin.ModelAdmin):
    """
    Add property media model in admin site
    """
    list_display = ['name', 'description']
    list_filter = ['name']


@admin.register(PropertyFeature)
class PropertyFeatureAdmin(admin.ModelAdmin):
    """
    Add property media model in admin site
    """
    list_display = ['name', 'description']
    list_filter = ['name']


@admin.register(PropertyReview)
class PropertyReviewAdmin(admin.ModelAdmin):
    """
    Add property review model in admin site
    """
    list_display = ['user', 'property', 'rate']
    list_filter = ['rate']


@admin.register(PropertyCategory)
class PropertyCategoryAdmin(admin.ModelAdmin):
    """
    Add property review model in admin site
    """
    list_display = ['name', 'description', 'slug']
    list_filter = ['name']
