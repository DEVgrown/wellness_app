from rest_framework.permissions import BasePermission, SAFE_METHODS


def _check_is_studio_admin(user):
    if not user or not user.is_authenticated:
        return False
    if user.is_staff or user.is_superuser:
        return True
    if hasattr(user, 'profile') and user.profile.is_studio_admin:
        return True
    return getattr(user, 'is_studio_admin', False)


def _check_is_coach(user):
    if not user or not user.is_authenticated:
        return False
    if _check_is_studio_admin(user):
        return True
    if hasattr(user, 'profile') and user.profile.is_coach:
        return True
    return getattr(user, 'is_coach', False)


class IsVerifiedStudioAdmin(BasePermission):
    """
    Grants access strictly to authenticated users with staff, superuser, or studio admin role.
    """
    def has_permission(self, request, view):
        return _check_is_studio_admin(request.user)


class IsClientUser(BasePermission):
    """Allows access to verified clients/members."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsCoachUser(BasePermission):
    """Allows access to coaches/practitioners and administrators."""
    def has_permission(self, request, view):
        return _check_is_coach(request.user)


class IsStudioAdminUser(BasePermission):
    """Allows access strictly to studio administrators and superusers."""
    def has_permission(self, request, view):
        return _check_is_studio_admin(request.user)


class IsOwnerOrAdmin(BasePermission):
    """Object-level permission ensuring users manage only their own profile, avatar, and bookings."""
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if _check_is_studio_admin(request.user):
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user
