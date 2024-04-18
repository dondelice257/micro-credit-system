from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission to only allow users with is_admin flag set to True.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user has is_admin flag set to True.
        """
        return request.user.is_authenticated and request.user.is_admin
