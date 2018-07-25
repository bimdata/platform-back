from django.db import models
from django.utils.encoding import force_bytes, smart_text
from django.contrib.auth import get_user_model
from django.db import transaction
import base64
import hashlib
from django.conf import settings
from django.contrib.postgres.fields import JSONField


class PlatformUser(models.Model):
    """ Represents a user managed by an OpenID Connect provider (OP). """

    # An OpenID Connect user is associated with a record in the main user table.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="paltform_user"
    )

    # The 'sub' value (aka Subject Identifier) is a locally unique and never reassigned identifier
    # within the issuer for the end-user. It is intended to be consumed by relying parties and does
    # not change over time. It corresponds to the only way to uniquely identify users between OIDC
    # provider and relying parties.
    sub = models.CharField(max_length=255, unique=True, verbose_name="Subject identifier")

    access_token = models.CharField(
        max_length=255, unique=True, verbose_name="Access Token", null=True, blank=True
    )
    refresh_token = models.CharField(
        max_length=255, unique=True, verbose_name="Refresh Token", null=True, blank=True
    )

    id_token = models.TextField(null=True, blank=True)

    # The content of the userinfo response will be stored in the following field.
    userinfo = JSONField(verbose_name="Subject extra data")

    class Meta:
        verbose_name = "OpenID Connect user"
        verbose_name_plural = "OpenID Connect users"

    def __str__(self):
        return str(self.user)

    @classmethod
    @transaction.atomic
    def create_oidc_user_from_claims(cls, claims, access_token, refresh_token, id_token):
        """
        Creates a ``PlatformUser`` instance using the claims extracted from an id_token.
        """
        sub = claims["sub"]
        email = claims["email"]
        username = base64.urlsafe_b64encode(hashlib.sha1(force_bytes(sub)).digest()).rstrip(
            b"="
        )
        user = get_user_model().objects.create_user(smart_text(username), email)
        platform_user = cls.objects.create(
            user=user,
            sub=sub,
            userinfo=claims,
            access_token=access_token,
            refresh_token=refresh_token,
            id_token=id_token,
        )
        return platform_user

    @transaction.atomic
    def update_oidc_user_from_claims(self, claims, access_token, refresh_token, id_token):
        """
        Updates a ``PlatformUser`` instance using the claims extracted from an id_token.
        """
        self.userinfo = claims
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.id_token = id_token
        self.save()
        self.user.email = claims["email"]
        self.user.save()
