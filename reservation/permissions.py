from rest_framework.permissions import BasePermission
from rest_framework import permissions


class CanAddOrUpdateReservation(BasePermission):
    """
    Custom permission class for admin or host user to make reservation
    """
    def has_permission(self, request, view):
        guest_user = bool(request.user and request.user.role == 'guest')
        admin_user = bool(request.user and request.user.is_superuser)
        return guest_user or admin_user
