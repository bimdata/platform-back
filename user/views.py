from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.response import Response


class AuthCallbackSerializer(serializers.Serializer):
    code = serializers.CharField()
    nonce = serializers.CharField()


@api_view(["POST"])
def back_callback(request):
    serializer = AuthCallbackSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    code = serializer.validated_data.get("code")
    nonce = serializer.validated_data.get("nonce")
    user = authenticate(request, code=code, nonce=nonce)

    if user:
        return Response("", status=status.HTTP_200_OK)

    return Response(
        {"error": "Unable to validate authentication"}, status=status.HTTP_400_BAD_REQUEST
    )
