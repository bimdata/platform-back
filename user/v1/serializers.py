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
