import logging
import requests
from requests.exceptions import HTTPError
from django.urls import reverse
from django.conf import settings
from mozilla_django_oidc import auth
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from django.core.exceptions import SuspiciousOperation
from rest_framework import exceptions
from user.models import User
from mozilla_django_oidc.utils import (
    absolutify,
    import_from_settings,
    parse_www_authenticate_header,
)


LOGGER = logging.getLogger(__name__)


class OIDCAuthenticationBackend(auth.OIDCAuthenticationBackend):
    def authenticate(self, request, **kwargs):
        """Authenticates a user based on the OIDC code flow."""
        self.request = request

        code = self.request.GET.get("code")
        nonce = self.request.GET.get("nonce")

        if not code:
            return None

        reverse_url = import_from_settings(
            "OIDC_AUTHENTICATION_CALLBACK_URL", "oidc_authentication_callback"
        )

        token_payload = {
            "client_id": self.OIDC_RP_CLIENT_ID,
            "client_secret": self.OIDC_RP_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": absolutify(self.request, reverse(reverse_url)),
        }

        # Get the token
        token_info = self.get_token(token_payload)
        id_token = token_info.get("id_token")
        refresh_token = token_info.get("refresh_token")

        # Validate the token
        payload = self.verify_token(id_token, nonce=nonce)

        if payload:
            try:
                return self.get_or_create_user(refresh_token, payload)
            except SuspiciousOperation as exc:
                LOGGER.warning("failed to get or create user: %s", exc)
                return None

        return None

    def get_or_create_user(self, refresh_token, user_info):
        """Returns a User instance if 1 user is found. Creates a user if not found
        and configured to do so. Returns nothing if multiple users are matched."""
        claims_verified = self.verify_claims(user_info)
        if not claims_verified:
            msg = "Claims verification failed"
            raise SuspiciousOperation(msg)

        sub = user_info.get("sub")
        try:
            user = self.UserModel.objects.get(sub=sub)
            return user
        except self.UserModel.DoesNotExist:
            return self.create_user(refresh_token, user_info)

    def create_user(self, refresh_token, claims):
        """Return object for a newly created user account."""

        sub = claims.get("sub")

        return self.UserModel.objects.create_user(
            username=sub, sub=sub, refresh_token=refresh_token
        )


class DrfOIDCAuthentication(OIDCAuthentication):
    def __init__(self, backend=None):
        # We're not using lib's init
        pass

    def authenticate(self, request):
        """
        Authenticate the request and return a tuple of (user, token) or None
        if there was no authentication attempt.
        """
        access_token = self.get_access_token(request)

        if not access_token:
            return None

        try:
            user_response = requests.get(
                settings.OIDC_OP_USER_ENDPOINT,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            user_response.raise_for_status()
        except HTTPError as exc:
            resp = exc.response

            # if the oidc provider returns 401, it means the token is invalid.
            # in that case, we want to return the upstream error message (which
            # we can get from the www-authentication header) in the response.
            if resp.status_code == 401 and "www-authenticate" in resp.headers:
                data = parse_www_authenticate_header(resp.headers["www-authenticate"])
                raise exceptions.AuthenticationFailed(data["error_description"])

            # for all other http errors, check other auth methods
            return None

        user_info = user_response.json()
        user = User.objects.filter(sub=user_info.get("sub")).first()
        if not user:
            msg = "Login failed: No user found for the given access token."
            raise exceptions.AuthenticationFailed(msg)

        return user, access_token
