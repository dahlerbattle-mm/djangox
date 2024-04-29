import urllib.parse

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import HttpResponse, redirect, render
from django.utils import timezone

from .models import OAuthCredentials
from .services import get_CSRF_token, getBearerToken, getRandomString
import logging
import requests
from datetime import timedelta
from urllib.parse import urlencode

# much of this is taken from https://github.com/IntuitDeveloper/OAuth2PythonSampleApp


def index(request):
    services = settings.INTEGRATION_SERVICES
    return render(request, "integrations/index.html", {'services': services})

@login_required
def quickbooks_auth(request): 
    state_token = get_CSRF_token(request)
    request.session['auth_state'] = state_token
    url = f"https://appcenter.intuit.com/connect/oauth2?client_id={settings.QUICKBOOKS_CLIENT_ID}&redirect_uri={settings.REDIRECT_URI}&response_type=code&scope=com.intuit.quickbooks.accounting&state={state_token}"
    print("Redirecting to URL:", url)  # Print the URL to debug
    return redirect(url)

@login_required
def quickbooks_callback(request): 
    auth_code = request.GET.get('code')
    token_url = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer'
    print("auth_code:", auth_code)
    try:
        auth_response = requests.post(token_url, data={
            'grant_type': 'authorization_code', 
            'code': auth_code,
            'redirect_uri': settings.REDIRECT_URI,
        }, auth=(settings.QUICKBOOKS_CLIENT_ID, settings.QUICKBOOKS_CLIENT_SECRET)).json()

        if 'error' in auth_response:
            logging.error(f"Error from QuickBooks: {auth_response['error']}")
            return redirect('error_page')  # Redirect to an error handling page or similar

        print("Quickbooks object", auth_response['access_token'], "created.")
        print("Expires:", timezone.now() + timedelta(seconds=auth_response['expires_in']))

        OAuthCredentials.objects.create(
            user=request.user,
            service='quickbooks',
            access_token=auth_response['access_token'],
            refresh_token=auth_response['refresh_token'],
            expiration_at=timezone.now() + timedelta(seconds=auth_response['expires_in'])
        )
    except Exception as e:
        logging.error(f"Exception in handling QuickBooks callback: {str(e)}")
        return redirect('profile')  # Redirect to an error handling page or similar

    return redirect('integrations')

@login_required
def hubspot_auth(request):
    state_token = get_CSRF_token(request)
    request.session['auth_state'] = state_token
    params = {
        'client_id': settings.HUBSPOT_CLIENT_ID,
        'redirect_uri': settings.HUBSPOT_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'crm.schemas.companies.read crm.schemas.companies.write crm.schemas.deals.read crm.schemas.deals.write',
        'state': state_token
    }
    url = f"https://app.hubspot.com/oauth/authorize?{urlencode(params)}"
    print("Redirecting to URL:", url)  # Print the URL to debug
    return redirect(url)

@login_required
def hubspot_callback(request):
    auth_code = request.GET.get('code')
    state_token = request.session.get('auth_state')
    received_state = request.GET.get('state')

    if not state_token or state_token != received_state:
        logging.error("Invalid state token")
        return redirect('error_page')  # Redirect to an error handling page

    token_url = 'https://api.hubapi.com/oauth/v1/token'
    print("auth_code:", auth_code)
    try:
        auth_response = requests.post(token_url, data={
            'grant_type': 'authorization_code',
            'client_id': settings.HUBSPOT_CLIENT_ID,
            'client_secret': settings.HUBSPOT_CLIENT_SECRET,
            'redirect_uri': settings.HUBSPOT_REDIRECT_URI,
            'code': auth_code
        }, headers={'Content-Type': 'application/x-www-form-urlencoded'}).json()

        if 'error' in auth_response:
            logging.error(f"Error from HubSpot: {auth_response['error']}")
            return redirect('error_page')  # Redirect to an error handling page or similar

        print("HubSpot access token", auth_response['access_token'], "created.")
        print("Expires:", timezone.now() + timedelta(seconds=auth_response['expires_in']))

        OAuthCredentials.objects.create(
            user=request.user,
            service='hubspot',
            access_token=auth_response['access_token'],
            refresh_token=auth_response['refresh_token'],
            expiration_at=timezone.now() + timedelta(seconds=auth_response['expires_in'])
        )
    except Exception as e:
        logging.error(f"Exception in handling QuickBooks callback: {str(e)}")
        return redirect('profile')  # Redirect to an error handling page or similar

    return redirect('integrations')