from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):  # Allow access only if the object belongs to the requesting user.

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated   # Check if the user is authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user     # Check if the object(expense) belongs to the requesting user