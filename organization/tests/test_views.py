from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.models import User


class TestCreateCloud(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(
            username="John Doe", first_name="John", last_name="Doe"
        )
        self.client.force_authenticate(user=self.user, token="don't care for now")

    # Need to patch where the function is used because it can be loaded before the mock
    @patch("organization.views.get_jwt_value", return_value=b"jwt-token")
    @patch("externals.keycloak.get_access_token", return_value="access-token")
    @patch(
        "bimdata_api_client.api.collaboration_api.CollaborationApi.create_cloud",
        return_value={"id": 456},
    )
    @patch(
        "bimdata_api_client.api.webhook_api.WebhookApi.create_web_hook",
        return_value={"id": 789},
    )
    def test_create_cloud(
        self, create_web_hook, create_cloud, get_access_token, get_jwt_value
    ):
        url = reverse("v1:create_cloud")
        body = {"organization_id": 123, "name": "Test"}

        response = self.client.post(url, data=body)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["cloud_id"] == 456
        create_cloud.assert_called_once()
        create_web_hook.assert_called_once()

    # def test_register_cloud(self):
    #   pass # TODO
