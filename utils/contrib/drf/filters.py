import coreapi
import warnings
from django_filters.rest_framework import DjangoFilterBackend


class FilterBackendWithQuerysetWorkaround(DjangoFilterBackend):
    def get_schema_fields(self, view):
        # This is not compatible with widgets where the query param differs from the
        # filter's attribute name. Notably, this includes `MultiWidget`, where query
        # params will be of the format `<name>_0`, `<name>_1`, etc...

        filter_class = getattr(view, "filter_class", None)
        if filter_class is None:
            try:
                queryset = view.get_queryset()
            except BaseException:
                queryset = view.serializer_class.Meta.model.objects.none()
            try:
                filter_class = self.get_filter_class(view, queryset)
            except BaseException:
                warnings.warn(
                    "{} is not compatible with schema generation".format(
                        view.__class__.__name__
                    )
                )
                filter_class = None

        return (
            []
            if not filter_class
            else [
                coreapi.Field(
                    name=field_name,
                    required=field.extra["required"],
                    location="query",
                    schema=self.get_coreschema_field(field),
                )
                for field_name, field in filter_class.base_filters.items()
            ]
        )
