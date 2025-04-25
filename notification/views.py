# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
import hashlib
import hmac

from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from notification.models import NotificationHistory
from notification.models import NotificationWebhook
from notification.models import Project
from notification.models import Subscription
from notification.permissions import IsProjectAdmin
from notification.serializers import ProjectWebhookSerializer
from notification.serializers import SubscriptionSerializer
from utils.views import get_or_404


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated, IsProjectAdmin])
def update_notifications(request, cloud_id, project_id):
    project, created = Project.objects.get_or_create(api_id=project_id, cloud_id=cloud_id)
    try:
        # update
        serializer = SubscriptionSerializer(
            instance=Subscription.objects.get(project=project),
            data=request.data,
            context={"project": project},
        )
    except Subscription.DoesNotExist:
        # create
        serializer = SubscriptionSerializer(data=request.data, context={"project": project})

    serializer.is_valid(raise_exception=True)
    subscription = serializer.save(project=project)
    subscription.update_webhooks()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated, IsProjectAdmin])
def get_notifications(request, cloud_id, project_id):
    project, created = Project.objects.get_or_create(api_id=project_id, cloud_id=cloud_id)
    subscription = get_or_404(Subscription, project=project)
    serializer = SubscriptionSerializer(instance=subscription, context={"project": project})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def webhook(request):
    req_signature = request.META.get("HTTP_X_BIMDATA_SIGNATURE")
    if not req_signature:
        raise ValidationError(detail={"x-bimdata-signature": "Header required"})

    raw_body = request.body

    serializer = ProjectWebhookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    project_id = serializer.validated_data["project_id"]
    webhook_id = serializer.validated_data["webhook_id"]
    webhook = get_or_404(NotificationWebhook, project_id=project_id, webhook_id=webhook_id)

    body_signature = hmac.new(webhook.secret.encode(), raw_body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(req_signature, body_signature):
        raise ValidationError(detail={"x-bimdata-signature": "Bad request signature"})

    event = serializer.validated_data["event_name"]
    payload = serializer.validated_data["data"]

    NotificationHistory.objects.create(
        project_id=webhook.project_id, event=event, payload=payload
    )
    return Response(status=status.HTTP_204_NO_CONTENT)
