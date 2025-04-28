# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

from user.models import Notification
from user.v1.serializers import NotificationSerializer


class NotificationViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    operations = {"list": "getSelfNotifications", "read": "getNotification"}

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user.fosuser)
