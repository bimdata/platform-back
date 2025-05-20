# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
import json
import re

from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import PeriodicTask
from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from notification.models import Subscription

TIME_VALIDATION = re.compile(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$")


class PeriodicTaskSerializer(serializers.Serializer):
    time = serializers.RegexField(TIME_VALIDATION)
    timezone = TimeZoneSerializerField()

    monday = serializers.BooleanField()
    tuesday = serializers.BooleanField()
    wednesday = serializers.BooleanField()
    thursday = serializers.BooleanField()
    friday = serializers.BooleanField()
    saturday = serializers.BooleanField()
    sunday = serializers.BooleanField()

    def to_representation(self, instance):
        # sunday is 0 or 7, monday is 1, tuesday is 2, ..., saturday is 6
        crontab = instance.crontab
        day_of_week = crontab.day_of_week
        return {
            "time": f"{crontab.hour}:{crontab.minute}",
            "timezone": str(crontab.timezone),
            "monday": "1" in day_of_week,
            "tuesday": "2" in day_of_week,
            "wednesday": "3" in day_of_week,
            "thursday": "4" in day_of_week,
            "friday": "5" in day_of_week,
            "saturday": "6" in day_of_week,
            "sunday": "0" in day_of_week or "7" in day_of_week,
        }


class SubscriptionSerializer(serializers.ModelSerializer):
    schedule = PeriodicTaskSerializer(source="periodic_task")

    class Meta:
        model = Subscription
        fields = (
            "id",
            "recipients_group_id",
            "schedule",
            "locale",
            "document_creation",
            "document_deletion",
            "folder_creation",
            "folder_deletion",
            "visa_creation",
            "visa_deletion",
            "visa_validation",
            "visa_denied",
            "bcf_topic_creation",
            "bcf_topic_deletion",
            "invitation_accepted",
            "model_creation",
            "model_deletion",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        """
        schedule_data looks like {
            "time": "09:00",
            "timezone": "Europe/Paris",
            "monday": False,
            "tuesday": False,
            "wednesday": False,
            "thursday": False,
            "friday": False,
            "saturday": False,
            "sunday": False,
        }
        """
        schedule_data = validated_data.pop("periodic_task")
        crontab = CrontabSchedule.objects.create(
            hour=schedule_data["time"].split(":")[0],
            minute=schedule_data["time"].split(":")[1],
            timezone=schedule_data["timezone"],
            day_of_week=self._schedule_data_to_day_of_week(schedule_data),
        )
        periodic_task = PeriodicTask.objects.create(
            crontab=crontab,
            name=f"Notification schedule for project {self.context["project"].api_id}",
            task="platform_back.tasks.notifications.send_project_notifications_email",
            kwargs=json.dumps(
                {
                    "project_id": self.context["project"].api_id,
                }
            ),
        )
        return Subscription.objects.create(**validated_data, periodic_task=periodic_task)

    def update(self, instance, validated_data):
        schedule_data = validated_data.pop("periodic_task")
        crontab = instance.periodic_task.crontab
        crontab.hour = schedule_data["time"].split(":")[0]
        crontab.minute = schedule_data["time"].split(":")[1]
        crontab.timezone = schedule_data["timezone"]
        crontab.day_of_week = self._schedule_data_to_day_of_week(schedule_data)
        crontab.save()
        instance = super().update(instance, validated_data)
        return instance

    def _schedule_data_to_day_of_week(self, schedule_data):
        return ",".join(
            [
                str(i)
                for i, day in enumerate(
                    [
                        "sunday",
                        "monday",
                        "tuesday",
                        "wednesday",
                        "thursday",
                        "friday",
                        "saturday",
                    ]
                )
                if schedule_data[f"{day}"]
            ]
        )


class ProjectWebhookSerializer(serializers.Serializer):
    event_name = serializers.CharField(required=True)
    cloud_id = serializers.IntegerField(required=True)
    project_id = serializers.IntegerField(required=True)
    webhook_id = serializers.IntegerField(required=True)
    data = serializers.JSONField(required=True)
