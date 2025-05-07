from django.conf import settings
from django.db.models.constants import LOOKUP_SEP
from django.db.models.sql.query import Query
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.openapi import AutoSchema
from oidc_auth.authentication import JSONWebTokenAuthentication


DEFAULT_ERRORS = {
    "400": "A required field is missing in the body",
    "401": "The authentication failed. Your token may be expired, missing or malformed",
    "403": "You don't have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource.",
    "404": "The resource does not exist or you don't have the right to see if the resource exists",
    "500": "Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we'll look at it shortly.",
}


def follow_model_related_lookup(model, lookup):
    """
    Follow a model lookup `foreignkey__foreignkey__field` in the same
    way that Django QuerySet.filter() does, returning the final model name.
    """
    query = Query(model)
    lookup_splitted = lookup.split(LOOKUP_SEP)
    path_info, _, _, _ = query.names_to_path(lookup_splitted, query.get_meta())
    return path_info[-1].join_field.related_model


class OperationIdException(Exception):
    pass


class BIMDataAutoSchema(AutoSchema):
    def _get_doc_view_or_action(self):
        def without_keys(d, keys):
            return {k: v for k, v in d.items() if k not in keys}

        method = self.method.lower()
        if action_map := self.view.action_map:
            action_map = without_keys(action_map, ["head"])
            action = self.view.action
            if list(action_map.values()).count(action) > 1:
                action = f"{action}/{self.method_mapping[method]}"
        elif method == "get" and self._is_list_view():
            action = "list"
        else:
            action = self.method_mapping[method]
        try:
            view_doc = self.view.docs[action]
        except (KeyError, AttributeError):
            return None
        return view_doc

    def is_deprecated(self):
        doc = self._get_doc_view_or_action()
        if doc and (deprecated := doc.get("deprecated")):
            return deprecated
        return False

    def get_scopes(self):
        if required_scopes := getattr(self.view, "required_alternate_scopes", None):
            if action_scopes := required_scopes.get(self.method.upper()):
                return f"Required scopes: {', '.join(action_scopes)}"
        return ""

    def get_description(self):
        doc = self._get_doc_view_or_action()
        scopes = self.get_scopes()
        if doc and (description := doc.get("description", "")):
            if description and scopes:
                return description + "\n\n" + scopes
            else:
                return description + scopes
        return scopes

    def get_summary(self):
        doc = self._get_doc_view_or_action()
        if doc and (summary := doc.get("summary")):
            return summary
        return None

    def get_operation_id(self):
        doc = self._get_doc_view_or_action()
        if doc is None or not (operation := doc.get("operation")):
            raise OperationIdException(
                f"OperationId is missing in ViewSet '{self.view.__class__.__name__}' for method {self.method}"
            )
        return operation

    def get_tags(self):
        """override this for custom behaviour"""
        if tags := getattr(self.view, "tags", None):
            return tags
        tokenized_path = self._tokenize_path()
        # use first non-parameter path part as tag
        return tokenized_path[:1]

    def _get_response_bodies(self):
        add_error_codes = ["500"]
        if not self.method == "GET":
            add_error_codes.append("400")

        if self.get_auth():
            add_error_codes.append("401")
            add_error_codes.append("403")

        if not (self.method == "GET" and self._is_list_view()):
            if len(list(filter(lambda _: _["in"] == "path", self._get_parameters()))):
                add_error_codes.append("404")
        response_bodies = {}
        for code in add_error_codes:
            response_bodies[code] = {"description": DEFAULT_ERRORS[code]}
        response_bodies |= super()._get_response_bodies()
        return dict(sorted(response_bodies.items()))


class BimdataConnectAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = JSONWebTokenAuthentication
    name = "BIMData_Connect"

    def get_security_definition(self, auto_schema):
        return {
            "type": "oauth2",
            "description": f"Use your own app to log in. You MUST add {settings.API_URL}/* if you are directly using the Swagger on the API",
            "flows": {
                "implicit": {
                    "authorizationUrl": settings.IAM_URL
                    + "/realms/bimdata/protocol/openid-connect/auth",
                    "scopes": {},
                },
                "clientCredentials": {
                    "tokenUrl": settings.IAM_URL
                    + "/realms/bimdata/protocol/openid-connect/token",
                    "scopes": {},
                },
            },
        }


def handle_swagger_generation(get_queryset):
    def func_wrapper(self, *args, **kwargs):
        if getattr(self, "swagger_fake_view", False):
            serializer = self.get_serializer()
            meta = getattr(serializer, "Meta", None)
            if meta:
                model = getattr(meta, "model", None)
                if model:
                    return model.objects.none()
            # fallback to parent serializer
            # Does not work with nested router
            return super().get_queryset(*args, **kwargs).none()
        return get_queryset(self, *args, **kwargs)

    return func_wrapper
