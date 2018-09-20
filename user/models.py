from django.db import models
from django.contrib.auth.models import AbstractUser
from externals.bimdata_api import ApiClient
from django.db import transaction


class User(AbstractUser):
    # The 'sub' value (aka Subject Identifier) is a locally unique and never reassigned
    # identifier within the issuer for the end-user. It is intended to be consumed by relying
    # parties and does not change over time. It corresponds to the only way to uniquely
    # identify users between OIDC provider and relying parties.
    sub = models.CharField(
        max_length=255, unique=True, db_index=True, verbose_name="Subject identifier"
    )
    refresh_token = models.CharField(
        max_length=255, verbose_name="Refresh Token", null=True, blank=True
    )
    demo_cloud = models.IntegerField(null=True, blank=True)
    demo_project = models.IntegerField(null=True, blank=True)

    company = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.sub}: {self.email}"

    def to_json(self):
        return {
            "email": self.email,
            "firstname": self.first_name,
            "lastname": self.last_name,
            "company": self.company,
        }

    @classmethod
    @transaction.atomic
    def create(cls, access_token=None, **kwargs):
        username = kwargs.get("sub")
        user = User.objects.create(username=username, **kwargs)
        client = ApiClient(access_token, user)
        cloud = client.cloud_api.create_cloud(cloud={"name": "Demo"})
        demo = client.cloud_api.create_demo(id=cloud.id)

        user.demo_cloud = cloud.id
        user.demo_project = demo.id
        user.save()
        return user


class Notification(models.Model):
    recipient = models.ForeignKey("User", on_delete=models.CASCADE)
    text = models.TextField()


from user.signals import *
