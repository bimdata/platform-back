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

    access_token = models.CharField(
        db_index=True, max_length=255, verbose_name="Access Token", null=True, blank=True
    )

    id_token = models.TextField(null=True, blank=True)

    refresh_token = models.CharField(
        max_length=255, verbose_name="Refresh Token", null=True, blank=True
    )
