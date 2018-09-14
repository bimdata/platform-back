from django.db import models
from django.contrib.auth.models import AbstractUser


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

    def to_json(self):
        return {
            "email": self.email,
            "firstname": self.first_name,
            "lastname": self.last_name,
            "company": self.company,
        }


class Notification(models.Model):
    recipient = models.ForeignKey("User", on_delete=models.CASCADE)
    text = models.TextField()


from user.signals import *
