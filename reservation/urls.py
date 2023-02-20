from django.urls import path, include
from reservation import views
from rest_framework_nested import routers

# Use drf nested router to register view set routes
router = routers.DefaultRouter()
router.register('reservations', views.ReservationViewSet, basename='reservations')

urlpatterns = [
    # Include view set routers
    path('reservations/', include(router.urls)),
]
