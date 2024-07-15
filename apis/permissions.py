from rest_framework import permissions


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow superusers to create objects.
    But allow any user to read them.
    """

    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Allow POST only for superusers
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return request.user and request.user.is_superuser

        return False
