from platform_back.settings.environ import env

IAM_URL = env("IAM_URL") + "/auth/realms/bimdata"

IAM_OP_TOKEN_ENDPOINT = f"{IAM_URL}/protocol/openid-connect/token"

OIDC_AUTH = {
    # Specify OpenID Connect endpoint. Configuration will be
    # automatically done based on the discovery document found
    # at <endpoint>/.well-known/openid-configuration
    "OIDC_ENDPOINT": IAM_URL,
    # Accepted audiences the ID Tokens can be issued to
    "OIDC_AUDIENCES": ("account"),
    # (Optional) Function that resolves id_token into user.
    # This function receives a request and an id_token dict and expects to
    # return a User object. The default implementation tries to find the user
    # based on username (natural key) taken from the 'sub'-claim of the
    # id_token.
    "OIDC_RESOLVE_USER_FUNCTION": "user.auth.get_user_by_id",
    # (Optional) Number of seconds in the past valid tokens can be issued (default 600)
    "OIDC_LEEWAY": 60 * 60,  # 60 minutes
    # (Optional) Time before signing keys will be refreshed (default 24 hrs)
    "OIDC_JWKS_EXPIRATION_TIME": 24 * 60 * 60,
    # (Optional) Time before bearer token validity is verified again (default 10 minutes)
    "OIDC_BEARER_TOKEN_EXPIRATION_TIME": 5 * 60,
    # (Optional) Token prefix in JWT authorization header (default 'JWT')
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
    # (Optional) Which Django cache to use
    "OIDC_CACHE_NAME": "default",
    # (Optional) A cache key prefix when storing and retrieving cached values
    "OIDC_CACHE_PREFIX": "oidc_auth.",
}
