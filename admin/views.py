from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ngettext

from externals.bimdata_api import ApiClient
from externals.keycloak import get_access_token
from webhooks.models import WebHook
from webhooks.utils import register_webhook


def register_webhooks(request):
    """
    Register missing webhooks
    """
    access_token = get_access_token()
    client = ApiClient(access_token)
    webhooks = WebHook.objects.all()

    cloud_ids = [
        cloud["id"]
        for cloud in client.collaboration_api.get_clouds()
        if cloud["id"] not in webhooks.values_list("cloud_id", flat=True)
    ]

    for cloud_id in cloud_ids:
        register_webhook(
            cloud_id=cloud_id,
            events=[
                "bcf.topic.creation",
                "visa.validation.add",
                "visa.validation.remove",
            ],
            access_token=access_token,
        )
    added = len(cloud_ids)
    if added:
        messages.success(
            request,
            ngettext(
                "%d new webhook was successfully registered.",
                "%d new webhooks were successfully registered.",
                added,
            )
            % added,
        )
    else:
        messages.info(request, "No new webhook to register.")
    return redirect("admin:webhooks_webhook_changelist")
