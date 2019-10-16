# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
import hmac
import hashlib
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from webhooks.handlers import route_webhook


class WebHookHandler(APIView):
    authentication_classes = tuple()

    def post(self, request, format=None):
        if not request.META.get("headers"):
            raise ValidationError(detail={"x-bimdata-signature": "Header required"})

        req_signature = request.META.get("headers").get("x-bimdata-signature")
        if not req_signature:
            raise ValidationError(detail={"x-bimdata-signature": "Header required"})

        body_signature = hmac.new(
            settings.WEBHOOKS_SECRET.encode(), request.body, hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(req_signature, body_signature):
            raise ValidationError(detail={"x-bimdata-signature": "Bad request signature"})

        route_webhook(request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)
