from django.urls import path, re_path
from user.v1.views import UserViewSet
from utils.doc import schema_view


app_name = "v1"

urlpatterns = [
    path("me", UserViewSet.as_view({"get": "retrieve"}), name="me"),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("doc", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
