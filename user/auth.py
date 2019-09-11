from django.conf import settings
from user.models import User
from rest_framework.authentication import get_authorization_header
from django.utils.encoding import smart_text


def get_jwt_value(request):
    auth = get_authorization_header(request).split()
    auth_header_prefix = settings.OIDC_AUTH.get("JWT_AUTH_HEADER_PREFIX").lower()

    if not auth or smart_text(auth[0].lower()) != auth_header_prefix:
        return None

    if len(auth) == 1:
        msg = _("Invalid Authorization header. No credentials provided")
        raise AuthenticationFailed(msg)
    elif len(auth) > 2:
        msg = _("Invalid Authorization header. Credentials string should not contain spaces.")
        raise AuthenticationFailed(msg)

    return auth[1]


def create_user(request, id_token):
    access_token = get_jwt_value(request).decode("utf-8")
    return User.create(
        access_token=access_token,
        email=id_token.get("email").lower(),
        first_name=id_token.get("given_name"),
        last_name=id_token.get("family_name"),
        sub=id_token.get("sub"),
    )


def get_user_by_id(request, id_token):
    try:
        return User.objects.get(sub=id_token.get("sub"))
    except User.DoesNotExist:
        if id_token.get("bimdata_connect_sub"):
            try:
                user = User.objects.get(legacy_sub=id_token.get("bimdata_connect_sub"))
                user.sub = id_token.get("sub")
                user.save()
                return user
            except User.DoesNotExist:
                return create_user(request, id_token)
        else:
            return create_user(request, id_token)
