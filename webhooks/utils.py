from django.conf import settings
from externals.bimdata_api import ApiClient


def register_webhook(cloud_id, access_token=None):
    client = ApiClient(access_token)
    webhook = client.application_api.create_web_hook(
        cloud_pk=cloud_id,
        data={
            "events": ["org.members", "ifc.process_update"],
            "url": f"{settings.PLATFORM_BACK_URL}/webhook",
            "secret": settings.WEBHOOKS_SECRET,
        },
    )
    return webhook
