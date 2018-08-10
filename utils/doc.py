from inflection import camelize
from django.conf import settings

from rest_framework.permissions import AllowAny

from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.views import get_schema_view
from drf_yasg.utils import get_consumes
from drf_yasg import openapi


API_INFO = openapi.Info(
    title="BIMData Platform",
    default_version="v1",
    description="BIMData Platform documentation",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@bimdata.io"),
    license=openapi.License(name="Copyright BIMData"),
)

schema_view = get_schema_view(
    public=True, permission_classes=(AllowAny,), url=settings.PLATFORM_BACK_URL
)


class CamelCaseOperationIDAutoSchema(SwaggerAutoSchema):
    def get_operation_id(self, operation_keys):
        action = operation_keys[-1]
        methode = operation_keys[-2]
        if hasattr(self.view, "operations"):
            operation_id = self.view.operations.get(
                f"{methode}/{action}", self.view.operations.get(action)
            )
        else:
            operation_id = None
        if not operation_id:
            operation_id = super().get_operation_id(operation_keys)
            camelize(operation_id, uppercase_first_letter=False)

        return operation_id

    def get_tags(self, operation_keys):
        if hasattr(self.view, "tags"):
            return self.view.tags
        return super().get_tags(operation_keys)

    def get_consumes(self):
        """Return the MIME types this endpoint can consume.

        :rtype: list[str]
        """
        return get_consumes(self.view.get_parsers())
