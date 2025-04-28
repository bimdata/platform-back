from requests.exceptions import HTTPError
from rest_framework import permissions

from externals.bimdata_api import api_request
from user.auth import get_jwt_value


class IsProjectAdmin(permissions.BasePermission):
    message = "You must be a project admin to perform this action"

    def has_permission(self, request, view):
        cloud_id = view.kwargs.get("cloud_id")
        project_id = view.kwargs.get("project_id")
        access_token = get_jwt_value(request).decode("utf-8")
        try:
            # response = client.collaboration_api.check_project_access(cloud_id, project_id)
            # The python code generation on april 28th 2025 (and before) has a bug when validating response, where it expects user_role to be a string instad of an int.
            response, json = api_request(
                "get",
                f"/cloud/{cloud_id}/project/{project_id}/check-access",
                access_token,
                raise_for_status=True,
            )
        except HTTPError:
            return False

        return json.get("user_role") == 100
