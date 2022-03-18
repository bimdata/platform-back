SWAGGER_SETTINGS = {
    "DEEP_LINKING": True,
    "DEFAULT_AUTO_SCHEMA_CLASS": "utils.doc.CamelCaseOperationIDAutoSchema",
    "DEFAULT_FILTER_INSPECTORS": ["utils.doc_inspectors.DjangoFilterDescriptionInspector"],
    "DOC_EXPANSION": "none",
    "OPERATIONS_SORTER": "alpha",
    "TAGS_SORTER": "alpha",
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "description": 'Copy/paste a valid access token here prefixed with "Bearer "',
            "name": "Authorization",
            "in": "header",
        }
    },
    "USE_SESSION_AUTH": False,
    "DEFAULT_INFO": "utils.doc.API_INFO",
    "DEFAULT_API_URL": "https://api.bimdata.io/doc",
}
