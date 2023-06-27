# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
import hmac
import json
import hashlib
from django.urls import reverse
from django.test import override_settings
from rest_framework.test import APITestCase
from rest_framework import status


class TestWebHooks(APITestCase):
    def test_without_signature(self):
        url = reverse("webhook-handler")

        response = self.client.post(url, data={})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @override_settings(WEBHOOKS_SECRET="123")
    def test_bad_signature(self):
        url = reverse("webhook-handler")

        response = self.client.post(url, data={}, HTTP_X_BIMDATA_SIGNATURE="456")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @override_settings(WEBHOOKS_SECRET="123")
    def test_good_signature(self):
        url = reverse("webhook-handler")

        data = {"event_name": "haha"}
        data_encoded = json.dumps(data).encode()
        signature = hmac.new("123".encode(), data_encoded, hashlib.sha256).hexdigest()

        response = self.client.post(
            url,
            data=data_encoded,
            HTTP_X_BIMDATA_SIGNATURE=signature,
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
