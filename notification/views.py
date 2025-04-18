# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from notification.models import Project
from notification.models import Subscription
from notification.permissions import IsProjectAdmin
from notification.serializers import SubscriptionSerializer
from utils.views import get_or_404


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated, IsProjectAdmin])
def update_notifications(request, cloud_id, project_id):
    project, created = Project.objects.get_or_create(api_id=project_id, cloud_id=cloud_id)
    try:
        # update
        subscription = Subscription.objects.get(project=project)
        serializer = SubscriptionSerializer(
            instance=subscription, data=request.data, context={"project": project}
        )
    except Subscription.DoesNotExist:
        # create
        serializer = SubscriptionSerializer(data=request.data, context={"project": project})

    serializer.is_valid(raise_exception=True)
    serializer.save(project=project)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated, IsProjectAdmin])
def get_notifications(request, cloud_id, project_id):
    project, created = Project.objects.get_or_create(api_id=project_id, cloud_id=cloud_id)
    subscription = get_or_404(Subscription, project=project)
    serializer = SubscriptionSerializer(instance=subscription, context={"project": project})
    return Response(serializer.data, status=status.HTTP_200_OK)
