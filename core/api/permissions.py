from rest_framework.permissions import BasePermission


class IsObjectOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, user):
        return user == request.user or request.user.is_superuser


class isObjOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
