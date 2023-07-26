import requests
from django.conf import settings
from django.core.cache import cache


VERSION = 1


def get_access_token():
    """Cache that memoizes the return value of a method for some time.
    Increment the cache_version everytime your method's implementation changes in such a way that it returns values
    that are not backwards compatible. For more information, see the Django cache documentation:
    https://docs.djangoproject.com/en/2.2/topics/cache/#cache-versioning
    """
    cached_value = cache.get("access_token", version=VERSION)
    if cached_value:
        return cached_value

    auth = {
        "client_id": settings.OIDC_CLIENT_ID,
        "client_secret": settings.OIDC_CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    response = requests.post(settings.IAM_OP_TOKEN_ENDPOINT, data=auth)
    response.raise_for_status()
    response = response.json()
    access_token = response.get("access_token")
    expires_in = response.get("expires_in") - 5  # 5 sec to be safe
    cache.set("access_token", access_token, timeout=expires_in, version=VERSION)
    return access_token
