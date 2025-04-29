from rest_framework import permissions

class IsSelfForWrite(permissions.BasePermission):
    """
    Custom permission:
    - Allow anyone to GET (read).
    - Allow only the user themselves to POST (create) or UPDATE (PUT/PATCH).
    """

    def has_permission(self, request, view):
        # Allow GET for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow POST only if the user is authenticated
        if request.method == 'POST':
            return request.user.is_authenticated

        # For PUT/PATCH, we will check object permissions later
        return True

    def has_object_permission(self, request, view, obj):
        # Allow GET for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow update only if the object (user) matches the logged-in user
        return obj == request.user
