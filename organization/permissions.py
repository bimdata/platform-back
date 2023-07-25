from rest_framework import permissions

from user.auth import Client


class IsSelfClient(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, Client):
            return request.user.is_self_client
        return False
