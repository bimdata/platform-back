# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from user.models import User, GuidedTour


class TestGuidedTour(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(
            username="John Doe", first_name="John", last_name="Doe"
        )
        self.client.force_authenticate(user=self.user, token="don't care for now")

    def test_create_success(self):
        url = reverse("tours-list")

        body = {"name": "PLATFORM_VISA"}

        response = self.client.post(url, data=body)

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_fail(self):
        url = reverse("tours-list")
        GuidedTour.objects.create(user=self.user, name="PLATFORM_VISA")

        body = {"name": "PLATFORM_VISA"}

        response = self.client.post(url, data=body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_read_success(self):
        url = reverse("tours-list")

        fakeUser = User.objects.create(
            username="Miles Davis", first_name="Miles", last_name="Davis"
        )
        GuidedTour.objects.create(user=fakeUser, name="PLATFORM_VISA")

        GuidedTour.objects.create(user=self.user, name="PLATFORM_VISA")

        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        assert len(data) == 1
