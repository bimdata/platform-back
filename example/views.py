import requests
from requests.exceptions import HTTPError
from django.conf import settings
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView, View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from oidc_rp.conf import settings as oidc_rp_settings
from example.models import PlatformUser
from oidc_rp.utils import validate_and_return_id_token


class IndexView(TemplateView):
    template_name = "index.html"


class LoginView(TemplateView):
    template_name = "login.html"


class CbView(TemplateView):
    template_name = "cb.html"


@method_decorator(csrf_exempt, name="dispatch")
# REMOVE THIS CSRF EXEMPT
class CatchResponseView(View):
    def post(self, request):
        # Tries to retrieve user information from the OP.
        try:
            payload = {
                "grant_type": "authorization_code",
                "client_id": oidc_rp_settings.CLIENT_ID,
                "client_secret": oidc_rp_settings.CLIENT_SECRET,
                "code": request.POST.get("code"),
                "redirect_uri": "http://127.0.0.1:8080/logged/",
            }
            token_response = requests.post(
                oidc_rp_settings.PROVIDER_TOKEN_ENDPOINT + "/", data=payload
            )
            token_response.raise_for_status()
        except HTTPError:
            raise PermissionDenied("Code seems invalid.")
        token_response_data = token_response.json()
        access_token = token_response_data.get("access_token")
        refresh_token = token_response_data.get("refresh_token")
        raw_id_token = token_response_data.get("id_token")

        id_token = validate_and_return_id_token(raw_id_token, request.POST.get("nonce"))

        # Fetches the user information from the userinfo endpoint provided by the OP.
        # If the id_token contains userinfo scopes and claims we don't have to hit the userinfo
        # endpoint.
        if oidc_rp_settings.ID_TOKEN_INCLUDE_USERINFO:
            userinfo_data = id_token
        else:
            # Fetches the user information from the userinfo endpoint provided by the OP.
            userinfo_response = requests.get(
                oidc_rp_settings.PROVIDER_USERINFO_ENDPOINT,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            userinfo_response.raise_for_status()
            userinfo_data = userinfo_response.json()

        # Tries to retrieve a corresponding user in the local database and creates it if applicable.
        try:
            platform_user = PlatformUser.objects.select_related("user").get(
                sub=userinfo_data.get("sub")
            )
        except PlatformUser.DoesNotExist:
            platform_user = PlatformUser.create_oidc_user_from_claims(
                userinfo_data, access_token, refresh_token, raw_id_token
            )
        else:
            PlatformUser.update_oidc_user_from_claims(
                platform_user, userinfo_data, access_token, refresh_token, raw_id_token
            )

        return HttpResponse("")


class SignUpView(RedirectView):
    def get_redirect_url(self):
        return "{url}?next={next}".format(
            url=settings.OIDC_RP_SIGNUP_URL,
            next=self.request.build_absolute_uri(reverse("oidc_auth_request")),
        )
