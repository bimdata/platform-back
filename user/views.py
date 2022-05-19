# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from rest_framework import status, permissions, viewsets, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from user.v1.serializers import GuidedTourSerializer
from user.auth import get_jwt_value
from user.models import GuidedTour


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])  # added code
def create_or_update_user(request):
    requestParsed = request
    breakpoint()
    if hasattr(request, "user_created"):
        access_token = get_jwt_value(request).decode("utf-8")
        request.user.create_demo(access_token)
        return Response("", status=status.HTTP_201_CREATED)
    return Response("", status=status.HTTP_200_OK)


class GuidedTourViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = GuidedTourSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GuidedTour.objects.select_related('user').filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
