# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
import bimdata_api_client
import requests
from bimdata_api_client.api import bcf_api
from bimdata_api_client.api import collaboration_api
from bimdata_api_client.api import model_api
from bimdata_api_client.api import webhook_api
from django.conf import settings


class ApiClient:
    def __init__(self, access_token):
        self.config = bimdata_api_client.Configuration(
            host=settings.API_URL,
        )

        if ssl_ca_cert := settings.SSL_CERT_FILE:
            self.config.ssl_ca_cert = ssl_ca_cert
        if access_token:
            # when we have a user access_token
            self.config.access_token = access_token

        self.client = bimdata_api_client.ApiClient(self.config)

        self.bcf_api = bcf_api.BcfApi(self.client)
        self.collaboration_api = collaboration_api.CollaborationApi(self.client)
        self.model_api = model_api.ModelApi(self.client)
        self.webhook_api = webhook_api.WebhookApi(self.client)


session = requests.Session()


def api_request(verb, path, access_token, raise_for_status=False, **kwargs):
    url = settings.API_URL + path

    response = session.request(
        method=verb,
        url=url,
        **kwargs,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if raise_for_status:
        response.raise_for_status()
    try:
        return response, response.json()
    except ValueError:
        return response, response.content
