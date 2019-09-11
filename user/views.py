from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.response import Response


@api_view(["POST"])
def create_or_update_user(request):
    # Empty route. All stuff is done in auth
    return Response("", status=status.HTTP_200_OK)
