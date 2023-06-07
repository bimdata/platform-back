# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from django.conf import settings
from django.urls import reverse
from externals.bimdata_api import ApiClient


def register_webhook(cloud_id, events, access_token=None):
    client = ApiClient(access_token)
    webhook = client.webhook_api.create_web_hook(
        cloud_pk=cloud_id,
        web_hook_request={
            "events": events,
            "url": settings.PLATFORM_BACK_URL + reverse("webhook-handler"),
            "secret": settings.WEBHOOKS_SECRET,
        },
    )
    return webhook
