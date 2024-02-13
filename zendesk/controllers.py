from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest, HttpResponseRedirect
import requests
from urllib.parse import urlencode
from .models import AccessToken

ZENDESK_SUBDOMAIN = "self4077"
ZENDESK_CLIENT_ID = "zdg-client2"
ZENDESK_CLIENT_SECRET = "a8c0ffb1c571af9fec7c2f329f494f6a02b1bb56a6946ad0ef3dbe671fdd08e8"
REDIRECT_URI = "http://localhost:8000/zendesk/oauth/callback"

def zendesk_oauth_connect(request: HttpRequest):
    parameters = urlencode(
        {
            "response_type": "code",
            "client_id": ZENDESK_CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "scope": "read",
        }
    )
    auth_url = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/oauth/authorizations/new?{parameters}"
    return HttpResponseRedirect(redirect_to=auth_url)

def zendesk_oauth_callback(request: HttpRequest):
    print(request)
    # Get the code parameter from the request
    code = request.GET.get('code', None)

    # Check if code is present
    if not code:
        return HttpResponseBadRequest("Code parameter is missing")

    # Make a POST request to Zendesk OAuth endpoint
    token_response = requests.post(
        f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/oauth/tokens",
        data={
            "grant_type": "authorization_code",
            "client_id": ZENDESK_CLIENT_ID,
            "client_secret": ZENDESK_CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "code": code,
            "scope": "read",
        },
    )

    # Check if the request was successful
    if token_response.status_code != 200:
        return HttpResponseBadRequest("Zendesk OAuth failed")

    # Parse the JSON response
    token_response_json = token_response.json()

    # Check if access_token is present in the response
    if "access_token" not in token_response_json:
        return HttpResponseBadRequest("Access token not found in response")

    # Extract the access token
    access_token = token_response_json["access_token"]

    # Store the access token
    token = AccessToken.objects.create(token=access_token, subdomain=ZENDESK_SUBDOMAIN)
    token.save()
    print(token_response_json)

    try:
        from airflow_integration.integration.task import create_fetch_task
        create_fetch_task(None, ZENDESK_SUBDOMAIN, token.token)
    except Exception as e:
        print(e)

    # Return the access token in a JSON response
    return JsonResponse({"access_token": access_token})