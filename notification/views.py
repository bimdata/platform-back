# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
import hashlib
import hmac

from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from notification.models import NotificationHistory
from notification.models import NotificationWebhook
from notification.models import Project
from notification.models import Subscription
from notification.permissions import IsProjectAdmin
from notification.serializers import ProjectWebhookSerializer
from notification.serializers import SubscriptionSerializer
from utils.views import get_or_404


class NotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsProjectAdmin]

    @extend_schema(
        tags=["project-notifications"],
        operation_id="getProjectNotifications",
        responses=SubscriptionSerializer,
    )
    def get(self, request, cloud_id, project_id, format=None):
        project, created = Project.objects.get_or_create(api_id=project_id, cloud_id=cloud_id)
        subscription = get_or_404(Subscription, project=project)
        serializer = SubscriptionSerializer(
            instance=subscription, context={"project": project}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["project-notifications"],
        operation_id="updateProjectNotifications",
        request=SubscriptionSerializer,
        responses=SubscriptionSerializer,
    )
    def put(self, request, cloud_id, project_id, format=None):
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
            serializer = SubscriptionSerializer(
                data=request.data, context={"project": project}
            )

        serializer.is_valid(raise_exception=True)
        if request.META.get("HTTP_REFERER"):
            referer = request.META.get("HTTP_REFERER").rstrip("/")
            subscription = serializer.save(project=project, referer=referer)
        else:
            subscription = serializer.save(project=project)
        subscription.update_webhooks()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["project-notifications"],
        operation_id="deleteProjectNotifications",
        responses=None,
    )
    def delete(self, request, cloud_id, project_id, format=None):
        project, created = Project.objects.get_or_create(api_id=project_id, cloud_id=cloud_id)
        subscription = get_or_404(Subscription, project=project)
        notifications = NotificationWebhook.objects.filter(project=project)
        for notification in notifications:
            notification.unregister()
        notifications.delete()
        NotificationHistory.objects.filter(project=project).delete()
        subscription.periodic_task.delete()
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["project-notifications"],
    operation_id="postProjectWebHook",
    request=ProjectWebhookSerializer,
    responses={status.HTTP_204_NO_CONTENT: None},
)
@api_view(["POST"])
def webhook(request):
    req_signature = request.META.get("HTTP_X_BIMDATA_SIGNATURE")
    if not req_signature:
        raise ValidationError(detail={"x-bimdata-signature": "Header required"})

    raw_body = request.body

    serializer = ProjectWebhookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    cloud_id = serializer.validated_data["cloud_id"]
    project_id = serializer.validated_data["project_id"]
    webhook_id = serializer.validated_data["webhook_id"]

    try:
        webhook = NotificationWebhook.objects.select_related("project").get(
            project_id__api_id=project_id, webhook_id=webhook_id
        )
    except NotificationWebhook.DoesNotExist:
        raise NotFound("Webhook not found")

    body_signature = hmac.new(webhook.secret.encode(), raw_body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(req_signature, body_signature):
        raise ValidationError(detail={"x-bimdata-signature": "Bad request signature"})

    # DO NOT MAKE ANY WRITE BEFORE THIS LINE as the signature was not verified

    project = webhook.project
    if project.cloud_id != cloud_id:
        # The project has been moved to another cloud
        project.cloud_id = cloud_id
        project.save()

    event = serializer.validated_data["event_name"]
    payload = serializer.validated_data["data"]

    NotificationHistory.objects.create(
        project_id=webhook.project_id, event=event, payload=payload
    )

    return Response(status=status.HTTP_204_NO_CONTENT)
