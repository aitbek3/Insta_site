from rest_framework import permissions
from rest_framework.permissions import BasePermission


class CheckOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 'ownerUser':
            return True
        return False


class CheckCRUD(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.user_role == 'ownerUser'


class CheckOwnerPost(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user