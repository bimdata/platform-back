import sys

sys.path.append("platform_back/settings/platform_back/")

from components.common import PLATFORM_BACK_URL
from components.common import STATIC_URL
from components.common import DEFAULT_AUTHENTICATION_CLASSES


def alpha_operation_sorter(endpoint):
    """sort endpoints first alphanumerically by path, then by method order"""
    path, path_regex, method, callback = endpoint
    method_priority = {"GET": 0, "POST": 1, "PUT": 2, "PATCH": 3, "DELETE": 4}.get(method, 5)

    # Sort like this:
    # /foo
    # /foo/{id}
    # /foo/bar
    # /foo/{id}/bar
    # /foo/{foo_id}/bar/{id}/c
    if path[-4:] in ("{id}", "{pk}"):
        # Prior for /foo/{id} over /foo/whatever
        path = path[:-4] + " "
    # Prior for /foo/{id}/bar over /foo/{foo_id}/bar/{id} but not /foo/bar
    path = path.replace("{id}/", "{!id}/").replace("{pk}/", "{!pk}/")

    return path, method_priority


SPECTACULAR_SETTINGS = {
    "TITLE": "BIMData Platform Back API",
    "DESCRIPTION": """This is the defintion of BIMData Platform API.
    It handles features specific of the BIMData Platform like favorites projects and spaces, guided tour and emails""",
    "TOS": "https://connect.bimdata.io/terms/active/",
    "CONTACT": {
        "name": "Support BIMData",
        "url": "https://bimdata.io/",
        "email": "support@bimdata.io",
    },
    "LICENSE": {
        "name": "Copyright BIMData.io",
    },
    "VERSION": "v1",
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "defaultModelsExpandDepth": 3,
        "defaultModelExpandDepth": 3,
        "defaultModelRendering": "model",
        "docExpansion": "none",
        "oauth2RedirectUrl": PLATFORM_BACK_URL
        + STATIC_URL
        + "drf_spectacular_sidecar/swagger-ui-dist/oauth2-redirect.html",
        "displayOperationId": True,
        "filter": True,
    },
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "ENABLE_LIST_MECHANICS_ON_NON_2XX": True,
    "AUTHENTICATION_WHITELIST": DEFAULT_AUTHENTICATION_CLASSES,
    "ENUM_NAME_OVERRIDES": {
        "SubscriptionLocaleEnum": "notification.models.Subscription.LOCALE_CHOICES",
    },
    "POSTPROCESSING_HOOKS": [],
    "SORT_OPERATIONS": alpha_operation_sorter,
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}
