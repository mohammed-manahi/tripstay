from django.urls import path, include
from property import views
from rest_framework_nested import routers

# Use drf nested router to register view set routes
router = routers.DefaultRouter()
router.register('properties', views.PropertyViewSet, basename='properties')

urlpatterns = [
    # Include view set routers
    path("", include(router.urls)),
]