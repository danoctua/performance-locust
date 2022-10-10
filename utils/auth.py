import os

import requests

from cache import memorize


SSO_TOKEN_URL = os.environ["SSO_TOKEN_URL"]
CLIENT_ID = os.environ["CLIENT_ID"]
GRANT_TYPE = os.environ["GRANT_TYPE"]

TOKEN_REQUEST_BODY = {
    "grant_type": GRANT_TYPE,
    "client_id": CLIENT_ID,
}

SSO_TOKEN_KEY_TEMPLATE = "SSO_{}"
DEFAULT_CACHE_TIMEOUT = 3600


def get_sso_token_cached(username: str) -> str:
    @memorize(key=SSO_TOKEN_KEY_TEMPLATE.format(username), period=DEFAULT_CACHE_TIMEOUT)
    def _get_sso_token() -> str:
        r = requests.post(url=SSO_TOKEN_URL, data={**TOKEN_REQUEST_BODY, "username": username})
        r.raise_for_status()
        data = r.json()
        return data["access_token"]

    return _get_sso_token()
