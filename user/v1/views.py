# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from rest_framework.response import Response
from rest_framework import permissions, viewsets, mixins, status
from user.v1.serializers import NotificationSerializer, UserSerializer
from user.models import Notification
from drf_yasg.utils import swagger_auto_schema


class NotificationViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    operations = {"list": "getSelfNotifications", "read": "getNotification"}

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user.fosuser)


class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_id="getSelfUser", responses={status.HTTP_200_OK: UserSerializer()}
    )
    def retrieve(self, request):
        serializer = UserSerializer(
            instance=request.user, context={"request": request, "view": self}
        )

        return Response(serializer.data)
