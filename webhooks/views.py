# This file is part of the BIMData Platform package.
# (c) BIMData support@bimdata.io
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
import hashlib
import hmac

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from webhooks.handlers import WebhookHandler


class WebHookView(APIView):
    authentication_classes = tuple()

    def post(self, request, format=None):
        req_signature = request.META.get("HTTP_X_BIMDATA_SIGNATURE")
        if not req_signature:
            raise ValidationError(detail={"x-bimdata-signature": "Header required"})

        body_signature = hmac.new(
            settings.WEBHOOKS_SECRET.encode(), request.body, hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(req_signature, body_signature):
            raise ValidationError(detail={"x-bimdata-signature": "Bad request signature"})

        handler = WebhookHandler(request.data)
        if handler.is_valid():
            handler.handle()

        return Response(status=status.HTTP_204_NO_CONTENT)
