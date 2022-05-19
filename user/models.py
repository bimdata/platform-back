# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
import requests
from django.contrib.auth.models import AbstractUser
from django.db import transaction, models
from django.conf import settings

from externals.bimdata_api import ApiClient


class User(AbstractUser):
    # The 'sub' value (aka Subject Identifier) is a locally unique and never reassigned
    # identifier within the issuer for the end-user. It is intended to be consumed by relying
    # parties and does not change over time. It corresponds to the only way to uniquely
    # identify users between OIDC provider and relying parties.
    legacy_sub = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
        verbose_name="Subject identifier",
        help_text="sub from BIMData Connect. Kept for backward compatibility",
    )

    sub = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        db_index=True,
        help_text="sub from Keycloak",
    )

    demo_cloud = models.IntegerField(null=True, blank=True)
    demo_project = models.IntegerField(null=True, blank=True)

    company = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.sub or self.legacy_sub}: {self.email}"

    def to_json(self):
        return {
            "email": self.email,
            "firstname": self.first_name,
            "lastname": self.last_name,
            "company": self.company,
        }

    @classmethod
    @transaction.atomic
    def create(cls, **kwargs):
        username = kwargs.get("sub")
        user = User.objects.create(username=username, **kwargs)
        return user

    def create_demo(self, access_token=None):
        client = ApiClient(access_token)
        cloud = client.collaboration_api.create_cloud(
            data={"name": f"{self.first_name} {self.last_name}"}
        )
        with open("demo_icon.png", "rb") as file:
            demo_icon = ("image", ("demo_icon.png", file))
            response = requests.patch(
                url=f"{settings.API_URL}/cloud/{cloud.id}",
                files=[demo_icon],
                headers={"Authorization": f"Bearer {access_token}"},
            )
        response.raise_for_status()

        demo = client.collaboration_api.create_demo(id=cloud.id)
        self.demo_cloud = cloud.id
        self.demo_project = demo.id
        self.save()


class Notification(models.Model):
    recipient = models.ForeignKey("User", on_delete=models.CASCADE)
    text = models.TextField()


class IfcMail(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    ifc_id = models.PositiveIntegerField()

    MAIL_SUCCESS = "S"
    MAIL_ERRORED = "E"
    MAIL_CHOICES = ((MAIL_SUCCESS, "success"), (MAIL_ERRORED, "failed"))

    last_sent = models.CharField(max_length=1, choices=MAIL_CHOICES)

    class Meta:
        unique_together = (("user", "ifc_id"),)


class GuidedTour(models.Model):
    PLATFORM_INTRO = 'PLATFORM_INTRO'
    PLATFORM_VISA = 'PLATFORM_VISA'
    NAME_CHOICES = [
        (PLATFORM_INTRO, 'PLATFORM_INTRO'),
        (PLATFORM_VISA, 'PLATFORM_VISA'),
    ]

    user = models.ForeignKey("User", on_delete=models.CASCADE)
    name = models.CharField(max_length=128, choices=NAME_CHOICES)

    class Meta:
        unique_together = (("user", "name"),)

from user.signals import *