from rest_framework.permissions import BasePermission

class IsVerifiedStudioAdmin(BasePermission):
    """
    Grants access strictly to authenticated users with staff or superuser flags.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_staff or request.user.is_superuser)
        )
