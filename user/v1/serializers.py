# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from user.models import FavoriteCloud
from user.models import FavoriteProject
from user.models import GuidedTour
from user.models import Notification
from user.models import User


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


class GuidedTourSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = GuidedTour
        fields = ("user", "name")
        validators = [
            UniqueTogetherValidator(queryset=GuidedTour.objects.all(), fields=("user", "name"))
        ]

    def to_representation(self, instance):
        return {"name": instance.name}


class FavoriteCloudSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteCloud
        fields = ("cloud_id",)


class FavoriteProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProject
        fields = ("project_id",)
