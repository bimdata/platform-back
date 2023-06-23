from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from user.auth import get_jwt_value
from externals.bimdata_api import ApiClient
from organization.serializers import CloudSerializer
from webhooks.utils import register_webhook
from bimdata_api_client.model.cloud_request import CloudRequest


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_cloud(request):
    serializer = CloudSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    access_token = get_jwt_value(request).decode("utf-8")
    client = ApiClient(access_token)
    cloud_request = CloudRequest(**serializer.validated_data)
    cloud = client.collaboration_api.create_cloud(cloud_request)
    register_webhook(
        cloud_id=cloud["id"],
        events=[
            "bcf.topic.creation",
            "visa.validation.add",
            "visa.validation.remove",
        ],
        access_token=access_token,
    )
    return Response(status=status.HTTP_201_CREATED)
