from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        """
        this custome permission returns True only if
        the method is GET, HEAD, OPTION or etc
        or the user is authenticated as admin
        """
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)