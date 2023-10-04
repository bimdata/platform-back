# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from user.models import User, GuidedTour, FavoriteCloud, FavoriteProject


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


class TestUserFavorites(APITestCase):
    def test_get_user_favorites(self):
        user1 = User.objects.create(
            username="John Doe", first_name="John", last_name="Doe"
        )
        user2 = User.objects.create(
            username="Louise Michel", first_name="Louise", last_name="Michel"
        )

        self.client.force_authenticate(user=user1, token="don't care for now")

        FavoriteCloud.objects.create(user=user1, cloud_id=1)
        FavoriteCloud.objects.create(user=user1, cloud_id=2)
        FavoriteCloud.objects.create(user=user2, cloud_id=3)
        FavoriteProject.objects.create(user=user1, project_id=123)
        FavoriteProject.objects.create(user=user2, project_id=456)
        FavoriteProject.objects.create(user=user2, project_id=789)

        url = reverse("fav")
        response = self.client.get(url, user=user1)
        json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert json.get("cloud_ids") is not None
        assert len(json["cloud_ids"]) == 2
        assert json.get("project_ids") is not None
        assert len(json["project_ids"]) == 1


class TestFavoriteCloud(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(
            username="John Doe", first_name="John", last_name="Doe"
        )
        self.client.force_authenticate(user=self.user, token="don't care for now")

    def test_read(self):
        user2 = User.objects.create(
            username="Louise Michel", first_name="Louise", last_name="Michel"
        )
        FavoriteCloud.objects.create(user=self.user, cloud_id=1)
        FavoriteCloud.objects.create(user=self.user, cloud_id=2)
        FavoriteCloud.objects.create(user=user2, cloud_id=3)

        url = reverse("fav-clouds-list")
        response = self.client.get(url, user=self.user)
        json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert json.get("cloud_ids") is not None
        assert len(json["cloud_ids"]) == 2

    def test_create(self):
        url = reverse("fav-clouds-list")
        body = { "cloud_id": 123 }
        response = self.client.post(url, data=body)
        json = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert json.get("cloud_ids") is not None
        assert len(json["cloud_ids"]) == 1
        assert json["cloud_ids"][0] == 123

    def test_delete_success(self):
        FavoriteCloud.objects.create(user=self.user, cloud_id=1)

        url = reverse("fav-clouds-detail", kwargs={"cloud_id": 1})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None

        url = reverse("fav-clouds-list")
        response = self.client.get(url)
        json = response.json()

        assert len(json["cloud_ids"]) == 0

    def test_delete_failure(self):
        url = reverse("fav-clouds-detail", kwargs={"cloud_id": 1})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestFavoriteProject(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(
            username="John Doe", first_name="John", last_name="Doe"
        )
        self.client.force_authenticate(user=self.user, token="don't care for now")

    def test_read(self):
        user2 = User.objects.create(
            username="Louise Michel", first_name="Louise", last_name="Michel"
        )
        FavoriteProject.objects.create(user=self.user, project_id=1)
        FavoriteProject.objects.create(user=self.user, project_id=2)
        FavoriteProject.objects.create(user=user2, project_id=3)

        url = reverse("fav-projects-list")
        response = self.client.get(url, user=self.user)
        json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert json.get("project_ids") is not None
        assert len(json["project_ids"]) == 2

    def test_create(self):
        url = reverse("fav-projects-list")
        body = { "project_id": 123 }
        response = self.client.post(url, data=body)
        json = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert json.get("project_ids") is not None
        assert len(json["project_ids"]) == 1
        assert json["project_ids"][0] == 123

    def test_delete_success(self):
        FavoriteProject.objects.create(user=self.user, project_id=1)

        url = reverse("fav-projects-detail", kwargs={"project_id": 1})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None

        url = reverse("fav-projects-list")
        response = self.client.get(url)
        json = response.json()

        assert len(json["project_ids"]) == 0

    def test_delete_failure(self):
        url = reverse("fav-projects-detail", kwargs={"project_id": 1})
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
