from bimdata_api_client.model.cloud_request import CloudRequest
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from externals.bimdata_api import ApiClient
from externals.keycloak import get_access_token
from organization.permissions import IsSelfClient
from organization.serializers import CloudSerializer
from organization.serializers import RegisterCloudSerializer
from user.auth import get_jwt_value
from webhooks.utils import register_webhook


@extend_schema(
    tags=["platform"],
    operation_id="createCloud",
    request=CloudSerializer,
    responses={status.HTTP_204_NO_CONTENT: None},
)
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
            "bcf.topic.update",
            "visa.validation.add",
            "visa.validation.remove",
        ],
        access_token=get_access_token(),
    )
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["platform"],
    operation_id="registerCloudWebhooks",
    description="""This view is exclusively used by the API after a cloud has been created through the payment route.""",
    request=RegisterCloudSerializer,
    responses={status.HTTP_204_NO_CONTENT: None},
)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, IsSelfClient])
def register_cloud(request):
    # To simplify the process, the API utilizes the platform_back client
    # to create the token.
    # Therefore, we need to use the IsSelfClient permission.
    serializer = RegisterCloudSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    access_token = get_access_token()
    register_webhook(
        cloud_id=serializer.validated_data.get("id"),
        events=[
            "bcf.topic.creation",
            "bcf.topic.update",
            "visa.validation.add",
            "visa.validation.remove",
        ],
        access_token=access_token,
    )
    return Response(status=status.HTTP_204_NO_CONTENT)
