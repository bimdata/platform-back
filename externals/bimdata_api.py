import requests
import bimdata_api_client
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class ApiClient:
    def __init__(self, access_token=None, user=None):
        self.config = bimdata_api_client.Configuration()
        self.config.host = settings.API_URL
        self.config.api_key_prefix["Authorization"] = "Bearer"
        if access_token:
            # when we have a valid access_token
            self.config.api_key["Authorization"] = access_token
        elif user:
            # We need to retrive an access_token
            token_payload = {
                "client_id": self.OIDC_RP_CLIENT_ID,
                "client_secret": self.OIDC_RP_CLIENT_SECRET,
                "grant_type": "refresh_token",
                "refresh_token": user.refresh_token,
            }

            # Get the token
            response = requests.post(settings.OIDC_OP_TOKEN_ENDPOINT, token_payload)
            self.config.api_key["Authorization"] = response.json.get("access_token")
        else:
            raise ImproperlyConfigured("access_token or user must be defined")

        self.client = bimdata_api_client.ApiClient(self.config)

        self.cloud_api = bimdata_api_client.CloudApi(self.client)
        self.project_api = bimdata_api_client.ProjectApi(self.client)
        self.checkplan_api = bimdata_api_client.CheckplanApi(self.client)
        self.ifc_api = bimdata_api_client.IfcApi(self.client)
        self.application_api = bimdata_api_client.ApplicationApi(self.client)
        self.user_api = bimdata_api_client.UserApi(self.client)
