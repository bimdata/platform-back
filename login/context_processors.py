from django.conf import settings


def oidc_client_id(request):
    return {"OIDC_RP_CLIENT_ID": settings.OIDC_RP_CLIENT_ID}
