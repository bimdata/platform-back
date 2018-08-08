import logging
from django.urls import reverse
from mozilla_django_oidc import auth
from mozilla_django_oidc.utils import absolutify, import_from_settings
from django.core.exceptions import SuspiciousOperation

LOGGER = logging.getLogger(__name__)


class OIDCAuthenticationBackend(auth.OIDCAuthenticationBackend):
    def authenticate(self, request, **kwargs):
        """Authenticates a user based on the OIDC code flow."""
        self.request = request

        code = self.request.GET.get("code")
        nonce = kwargs.pop("nonce", None)

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
        access_token = token_info.get("access_token")
        refresh_token = token_info.get("refresh_token")

        # Validate the token
        payload = self.verify_token(id_token, nonce=nonce)

        if payload:
            try:
                return self.get_or_create_user(access_token, id_token, refresh_token, payload)
            except SuspiciousOperation as exc:
                LOGGER.warning("failed to get or create user: %s", exc)
                return None

        return None

    def get_or_create_user(self, access_token, id_token, refresh_token, user_info):
        """Returns a User instance if 1 user is found. Creates a user if not found
        and configured to do so. Returns nothing if multiple users are matched."""
        claims_verified = self.verify_claims(user_info)
        if not claims_verified:
            msg = "Claims verification failed"
            raise SuspiciousOperation(msg)

        sub = user_info.get("sub")
        try:
            user = self.UserModel.objects.get(sub=sub)
            return self.update_user(user, user_info)
        except self.UserModel.DoesNotExist:
            return self.create_user(access_token, id_token, refresh_token, user_info)

    def update_user(self, user, claims):
        """Update existing user with new claims, if necessary save, and return user"""
        user.access_token = claims.get("access_token")
        user.id_token = claims.get("id_token")
        user.save()
        return user

    def create_user(self, access_token, id_token, refresh_token, claims):
        """Return object for a newly created user account."""

        sub = claims.get("sub")

        return self.UserModel.objects.create_user(
            username=sub,
            sub=sub,
            access_token=access_token,
            id_token=id_token,
            refresh_token=refresh_token,
        )
