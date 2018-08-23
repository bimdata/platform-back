from django.views.generic import TemplateView, RedirectView
from django.contrib.auth import authenticate
from django.conf import settings
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.response import Response


class IndexView(TemplateView):
    template_name = "index.html"


class LoginView(TemplateView):
    template_name = "login.html"


class FrontCallbackView(TemplateView):
    template_name = "front_callback.html"


class SignUpView(RedirectView):
    def get_redirect_url(self):
        return "{url}?next={next}".format(
            url=settings.OIDC_OP_SIGNUP_URL,
            next=self.request.build_absolute_uri(reverse("oidc_authentication_init")),
        )


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
