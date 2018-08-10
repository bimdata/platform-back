from django.conf import settings


def oidc_settings(request):
    return {
        "OIDC_RP_CLIENT_ID": settings.OIDC_RP_CLIENT_ID,
        "OIDC_AUTH_REQUEST_RESPONSE_TYPE": settings.OIDC_AUTH_REQUEST_RESPONSE_TYPE,
        "OIDC_AUTHENTICATION_CALLBACK_URL": settings.OIDC_AUTHENTICATION_CALLBACK_URL,
        "OIDC_OP_ISSUER": settings.OIDC_OP_ISSUER,
        "OIDC_RP_SCOPES": settings.OIDC_RP_SCOPES,
        "API_URL": settings.API_URL,
    }
