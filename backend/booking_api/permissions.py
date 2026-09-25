from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsVerifiedStudioAdmin(BasePermission):
    """
    Grants access strictly to authenticated users with staff or superuser flags.
    Maintained for Phase 1 backward compatibility.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_staff or request.user.is_superuser or (hasattr(request.user, 'is_studio_admin') and request.user.is_studio_admin))
        )


class IsClientUser(BasePermission):
    """Allows access to verified clients/members."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'is_client', True))


class IsCoachUser(BasePermission):
    """Allows access to coaches/practitioners and administrators."""
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and 
            (getattr(request.user, 'is_coach', False) or getattr(request.user, 'is_studio_admin', False) or request.user.is_staff)
        )


class IsStudioAdminUser(BasePermission):
    """Allows access strictly to studio administrators and superusers."""
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and 
            (getattr(request.user, 'is_studio_admin', False) or request.user.is_staff or request.user.is_superuser)
        )


class IsOwnerOrAdmin(BasePermission):
    """Object-level permission ensuring users manage only their own profile, avatar, and bookings."""
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if getattr(request.user, 'is_studio_admin', False) or request.user.is_staff or request.user.is_superuser:
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user
