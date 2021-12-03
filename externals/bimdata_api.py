# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
import requests
import bimdata_api_client
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class ApiClient:
    def __init__(self, access_token=None):
        self.config = bimdata_api_client.Configuration()
        self.config.host = settings.API_URL
        if access_token:
            # when we have a user access_token
            self.config.access_token = access_token
        else:
            raise AuthenticationFailed("Making a request to the api without a user access token is not implemented.")

        self.client = bimdata_api_client.ApiClient(self.config)

        self.collaboration_api = bimdata_api_client.CollaborationApi(self.client)
        self.ifc_api = bimdata_api_client.IfcApi(self.client)
        self.webhook_api = bimdata_api_client.WebhookApi(self.client)
