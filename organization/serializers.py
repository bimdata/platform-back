from rest_framework import serializers


class CloudSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField(
        write_only=True,
        required=False,
    )
    name = serializers.CharField(max_length=255)


class CloudIdSerializer(serializers.Serializer):
    cloud_id = serializers.IntegerField(required=True)


class RegisterCloudSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
