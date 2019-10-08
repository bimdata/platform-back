# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from rest_framework import serializers
from user.models import User, Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "text")
        read_only_fields = ("id", "text")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "demo_cloud", "demo_project")
        read_only_fields = ("id", "demo_cloud", "demo_project")
