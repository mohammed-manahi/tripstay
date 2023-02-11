from django.urls import path, include
from property import views
from rest_framework_nested import routers

# Use drf nested router to register view set routes
router = routers.DefaultRouter()
router.register('properties', views.PropertyViewSet, basename='properties')
router.register('categories', views.CategoryViewSet, basename='categories')

# Define nested router for property media
property_router = routers.NestedDefaultRouter(router, 'properties', lookup='property')
property_router.register('media', views.MediaViewSet, basename='property-media')

urlpatterns = [
    # Include view set routers
    path('', include(router.urls)),
    # Include view set nested routers
    path('', include(property_router.urls)),
]
