import base64
import json
import random
import requests
from django.conf import settings


def getBearerToken(auth_code: str):
    # TODO: token_endpoint should technically be in environment variables
    token_endpoint = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    # TODO: this client_id and secret **might** need to come from the user, otherwise, put in settings
    client_id = settings.QUICKBOOKS_CLIENT_ID
    client_secret = settings.QUICKBOOKS_CLIENT_SECRET

    auth_header = "Basic " + stringToBase64(client_id + ":" + client_secret)
    headers = {
        "Accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": auth_header,
    }
    payload = {
        "code": auth_code,
        "redirect_uri": "http://localhost:8000/integrations/quickbooks/redirect",  # not sure why they need redirect here
        "grant_type": "authorization_code",
    }
    r = requests.post(token_endpoint, data=payload, headers=headers)
    if r.status_code != 200:
        return {"error": r.text}
    bearer_raw = json.loads(r.text)

    if "id_token" in bearer_raw:
        idToken = bearer_raw["id_token"]
    else:
        idToken = None

    return {
        "refresh_exp": bearer_raw["x_refresh_token_expires_in"],
        "access_token": bearer_raw["access_token"],
        "token_type": bearer_raw["token_type"],
        "refresh_token": bearer_raw["refresh_token"],
        "access_exp": bearer_raw["expires_in"],
        "id_token": idToken,
    }


def stringToBase64(s):
    return base64.b64encode(bytes(s, "utf-8")).decode()


# Returns a securely generated random string. Source from the django.utils.crypto module.
def getRandomString(
    length,
    allowed_chars="abcdefghijklmnopqrstuvwxyz" "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
):
    return "".join(random.choice(allowed_chars) for _ in range(length))


# Create a random secret key. Source from the django.utils.crypto module.
def getSecretKey():
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return getRandomString(40, chars)


def get_CSRF_token(request):
    token = request.session.get("csrfToken", None)
    if token is None:
        token = getSecretKey()
        request.session["csrfToken"] = token
    return token