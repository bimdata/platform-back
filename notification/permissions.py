from bimdata_api_client import ApiException
from rest_framework import permissions

from externals.bimdata_api import ApiClient
from user.auth import get_jwt_value


class IsProjectAdmin(permissions.BasePermission):
    message = "You must be a project admin to perform this action"

    def has_permission(self, request, view):
        cloud_id = view.kwargs.get("cloud_id")
        project_id = view.kwargs.get("project_id")
        access_token = get_jwt_value(request).decode("utf-8")
        client = ApiClient(access_token)
        try:
            access = client.collaboration_api.checkProjectAccess(cloud_id, project_id)
        except ApiException:
            return False
        return access.user_role == 100
