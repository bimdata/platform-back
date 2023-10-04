# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from user.auth import get_jwt_value
from user.models import GuidedTour, FavoriteCloud, FavoriteProject
from user.v1.serializers import GuidedTourSerializer, FavoriteCloudSerializer, FavoriteProjectSerializer
from utils.log import log_user_connect


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@log_user_connect
def create_or_update_user(request):
    if hasattr(request, "user_created"):
        access_token = get_jwt_value(request).decode("utf-8")
        request.user.create_demo(access_token)
        return Response("", status=status.HTTP_201_CREATED)
    return Response("", status=status.HTTP_200_OK)


class GuidedTourViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    serializer_class = GuidedTourSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GuidedTour.objects.select_related("user").filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_user_favorites(request):
    cloud_ids = FavoriteCloud.objects.filter(user=request.user).values_list("cloud_id", flat=True)
    project_ids = FavoriteProject.objects.filter(user=request.user).values_list("project_id", flat=True)
    return Response({"cloud_ids": cloud_ids, "project_ids": project_ids})


class FavoriteCloudViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin
):
    serializer_class = FavoriteCloudSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "cloud_id"
    queryset = FavoriteCloud.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        cloud_ids = super().list(request, *args, **kwargs).data
        return Response({"cloud_ids": cloud_ids})

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        cloud_ids = self.get_queryset().values_list("cloud_id", flat=True)
        return Response({"cloud_ids": cloud_ids}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteProjectViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin
):
    serializer_class = FavoriteProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "project_id"
    queryset = FavoriteProject.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        project_ids = super().list(request, *args, **kwargs).data
        return Response({"project_ids": project_ids})

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        project_ids = self.get_queryset().values_list("project_id", flat=True)
        return Response({"project_ids": project_ids}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
