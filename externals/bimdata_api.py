# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
import bimdata_api_client
from bimdata_api_client.api import collaboration_api, ifc_api, webhook_api, bcf_api
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class ApiClient:
    def __init__(self, access_token=None):
        self.config = bimdata_api_client.Configuration(
            host=settings.API_URL,
        )

        if ssl_ca_cert := settings.SSL_CERT_FILE:
            self.config.ssl_ca_cert = ssl_ca_cert
        if access_token:
            # when we have a user access_token
            self.config.access_token = access_token
        else:
            raise AuthenticationFailed(
                "Making a request to the api without a user access token is not implemented."
            )

        self.client = bimdata_api_client.ApiClient(self.config)

        self.bcf_api = bcf_api.BcfApi(self.client)
        self.collaboration_api = collaboration_api.CollaborationApi(self.client)
        self.ifc_api = ifc_api.IfcApi(self.client)
        self.webhook_api = webhook_api.WebhookApi(self.client)
