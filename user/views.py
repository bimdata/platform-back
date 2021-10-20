# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


@api_view(["POST"])
def create_or_update_user(request):
    # Empty route. All stuff is done in auth
    if hasattr(request, 'user_created'):
        return Response("", status=status.HTTP_201_CREATED)
    return Response("", status=status.HTTP_200_OK)
