# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from django.conf import settings
from django.utils.encoding import smart_str
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from user.models import User
from utils.log import log_user_first_connection


class Client:
    # hack for compatibility with user permissions
    # This is used in the register_cloud view.
    is_authenticated = True

    def __init__(self, *args, **kwargs):
        self.is_self_client = kwargs.get("is_self_client", False)


def get_jwt_value(request):
    auth = get_authorization_header(request).split()
    auth_header_prefix = settings.OIDC_AUTH.get("JWT_AUTH_HEADER_PREFIX").lower()

    if not auth or smart_str(auth[0].lower()) != auth_header_prefix:
        return None

    if len(auth) == 1:
        msg = "Invalid Authorization header. No credentials provided"
        raise AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = "Invalid Authorization header. Credentials string should not contain spaces."
        raise AuthenticationFailed(msg)

    return auth[1]


@log_user_first_connection
def create_user(request, id_token):
    return User.create(
        email=id_token.get("email").lower(),
        first_name=id_token.get("given_name"),
        last_name=id_token.get("family_name"),
        sub=id_token.get("sub"),
        language=id_token.get("locale"),
        initial_referer=request.META.get("HTTP_REFERER").rstrip("/"),
    )


def get_user_by_id(request, id_token):
    if client_id := id_token.get("clientId", id_token.get("client_id")):
        is_self_client = client_id == settings.OIDC_CLIENT_ID
        return Client(is_self_client=is_self_client)

    try:
        user = User.objects.get(sub=id_token.get("sub"))
        if user.language != id_token.get("locale"):
            user.language = id_token.get("locale")
            user.save()
        return user
    except User.DoesNotExist:
        user = create_user(request, id_token)
        setattr(request, "user_created", True)
        return user
