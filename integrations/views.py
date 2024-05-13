from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import HttpResponse, redirect, render
from django.utils import timezone

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from hubspot.auth.oauth import ApiException
from hubspot.utils.oauth import get_auth_url
from hubspot import HubSpot
import os

from datetime import timedelta
from urllib.parse import urlencode

from .models import OAuthCredentials
from .services import get_CSRF_token, getBearerToken, getRandomString
import logging
import requests

# much of this is taken from https://github.com/IntuitDeveloper/OAuth2PythonSampleApp


def index(request):
    services = settings.INTEGRATION_SERVICES
    return render(request, "integrations/index.html", {'services': services})

@login_required
def quickbooks_auth2(request):
    try: 
        environment="sandbox" # "sandbox" or "production"
        auth_client = AuthClient(settings.QUICKBOOKS_CLIENT_ID, settings.QUICKBOOKS_CLIENT_SECRET, settings.QUICKBOOKS_REDIRECT_URI , environment)
        url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
        print("Redirecting to URL:", url)  # Print the URL to debug
        return redirect(url)
    
    except Exception as e:
        # Log the error for troubleshooting
        print(f"Error in QuickBooks Auth: {str(e)}")
        # Redirect user to some error page
        return redirect('profile')

@login_required
def quickbooks_callback2(request):
    try:
        # Assuming you retrieve auth_code and realm_id from the callback URL parameters
        auth_code = request.GET.get('code')
        realm_id = request.GET.get('realmId')
        # print("Realm ID:", realm_id)
        # username = request.user  # Assuming you have a user object
        environment="sandbox" # "sandbox" or "production"
        
        auth_client = AuthClient(settings.QUICKBOOKS_CLIENT_ID, settings.QUICKBOOKS_CLIENT_SECRET, settings.QUICKBOOKS_REDIRECT_URI, environment)
        auth_client.get_bearer_token(auth_code, realm_id=realm_id)
        
        expiration_at = timezone.now() + timezone.timedelta(seconds=auth_client.expires_in)

        OAuthCredentials.objects.create(
            user=request.user,
            service='quickbooks',
            access_token=auth_client.access_token,
            refresh_token=auth_client.refresh_token,
            realm_id=auth_client.realm_id, #request.GET.get('realm_id', ''),
            expiration_at=expiration_at
        )
        print("Realm ID:", str(auth_client.realm_id))
        
        # Redirect user to some page indicating successful connection
        return redirect('integrations')
    
    except Exception as e:
        # Log the error for troubleshooting
        print(f"Error in QuickBooks callback: {str(e)}")
        # Redirect user to some error page
        return redirect('profile')

@login_required
def hubspot_auth(request):
    state_token = get_CSRF_token(request)
    request.session['auth_state'] = state_token
    params = {
        'client_id': settings.HUBSPOT_CLIENT_ID,
        'redirect_uri': settings.HUBSPOT_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'crm.objects.deals.read crm.objects.companies.read', 
        'state': state_token
    }
    url = f"https://app.hubspot.com/oauth/authorize?{urlencode(params)}"
    print("Redirecting to URL:", url)  # Print the URL to debug
    return redirect(url)

@login_required
def hubspot_callback2(request):
    code = request.GET.get('code')
    if not code:
        return redirect('profile')  # Redirect if no code is present

    api_client = HubSpot()
    try:
        tokens = api_client.auth.oauth.tokens_api.create(
            grant_type="authorization_code",
            redirect_uri=settings.HUBSPOT_REDIRECT_URI,
            client_id=settings.HUBSPOT_CLIENT_ID,
            client_secret=settings.HUBSPOT_CLIENT_SECRET,
            code=code
        )
    except ApiException as e:
        print(f"Exception when calling create_token method: {str(e)}")
        return redirect('profile')

    # Calculate expiration time for the access token
    expiration_at = timezone.now() + timezone.timedelta(seconds=tokens.expires_in)

    # Create and save the new OAuth credential record
    OAuthCredentials.objects.create(
        user=request.user,
        service='hubspot',
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        expiration_at=expiration_at
    )
    return redirect('integrations')  # Redirect to a success page, not the tokens object


@login_required
def jira_auth(request):
    state_token = get_CSRF_token(request)
    request.session['auth_state'] = state_token
    params = {
        'client_id': settings.JIRA_CLIENT_ID,
        'redirect_uri': settings.JIRA_REDIRECT_URI,
        'audience' : 'api.atlassian.com',
        'response_type': 'code',
        'state': state_token,
        'prompt' : 'consent',
        'scope' : 'read%3Ame%20read%3Aaccount',
    }
    url = f"https://auth.atlassian.com/authorize?{urlencode(params)}"
    print("Redirecting to URL:", url)  # Print the URL to debug
    return redirect(url)

#https://app.hubspot.com/oauth/authorize?client_id=22687d80-052b-42fe-93f6-9418fdd77803&redirect_uri=https://officially-fast-condor.ngrok-free.app/integrations/callback/hubspot/&scope=crm.schemas.quotes.read%20cms.functions.read%20crm.objects.line_items.read%20crm.schemas.deals.read%20crm.schemas.line_items.read%20cms.knowledge_base.articles.read%20cms.knowledge_base.settings.read%20collector.graphql_schema.read%20business-intelligence%20oauth%20crm.objects.owners.read%20conversations.read%20crm.export%20cms.performance.read%20e-commerce%20crm.objects.marketing_events.read%20crm.schemas.custom.read%20business_units_view.read%20crm.objects.custom.read%20crm.objects.feedback_submissions.read%20crm.objects.goals.read%20crm.objects.companies.read%20crm.lists.read%20crm.objects.deals.read%20crm.schemas.contacts.read%20crm.objects.contacts.read%20cms.domains.read%20crm.schemas.companies.read%20crm.objects.quotes.read
@login_required
def jira_callback(request):
    auth_code = request.GET.get('code')
    state_token = request.session.get('auth_state')
    received_state = request.GET.get('state')

    if not state_token or state_token != received_state:
        logging.error("Invalid state token")
        return redirect('profile')  # Redirect to an error handling page

    token_url = 'https://auth.atlassian.com/authorize'
    print("auth_code:", auth_code)
    try:
        auth_response = requests.post(token_url, data={
            'grant_type': 'authorization_code',
            'client_id': settings.JIRA_CLIENT_ID,
            'client_secret': settings.JIRA_CLIENT_SECRET,
            'redirect_uri': settings.JIRA_REDIRECT_URI,
            'code': auth_code
        }, headers={'Content-Type': 'application/x-www-form-urlencoded'}).json()

        if 'error' in auth_response:
            logging.error(f"Error from Jira: {auth_response['error']}")
            return redirect('profile')  # Redirect to an error handling page or similar

        print("Atlassian access token", auth_response['access_token'], "created.")
        print("Expires:", timezone.now() + timedelta(seconds=auth_response['expires_in']))

        OAuthCredentials.objects.create(
            user=request.user,
            service='jira',
            access_token=auth_response['access_token'],
            refresh_token=auth_response['refresh_token'],
            expiration_at=timezone.now() + timedelta(seconds=auth_response['expires_in'])
        )
    except Exception as e:
        logging.error(f"Exception in handling Jira callback: {str(e)}")
        return redirect('profile')  # Redirect to an error handling page or similar

    return redirect('integrations')


@login_required
def stripe_auth(request):
    state_token = get_CSRF_token(request)
    request.session['auth_state'] = state_token
    params = {
        'client_id': settings.STRIPE_CLIENT_ID,
        'redirect_uri': settings.STRIPE_REDIRECT_URI,
        'response_type': 'code',
        'state': state_token,
    }
    url = f"https://connect.stripe.com/oauth/authorize?{urlencode(params)}"
    print("Redirecting to URL:", url)  # Print the URL to debug
    return redirect(url)

@login_required
def stripe_callback(request):
    auth_code = request.GET.get('code')
    state_token = request.session.get('auth_state')
    received_state = request.GET.get('state')

    if not state_token or state_token != received_state:
        logging.error("Invalid state token")
        return redirect('profile')  # Redirect to an error handling page

    token_url = 'https://connect.stripe.com/oauth/authorize'
    print("auth_code:", auth_code)
    try:
        auth_response = requests.post(token_url, data={
            'grant_type': 'authorization_code',
            'client_id': settings.STRIPE_CLIENT_ID,
            'client_secret': settings.STRIPE_CLIENT_SECRET,
            'redirect_uri': settings.STRIPE_REDIRECT_URI,
            'code': auth_code
        }, headers={'Content-Type': 'application/x-www-form-urlencoded'}).json()

        if 'error' in auth_response:
            logging.error(f"Error from Stripe: {auth_response['error']}")
            return redirect('profile')  # Redirect to an error handling page or similar

        print("Stripe access token", auth_response['access_token'], "created.")
        print("Expires:", timezone.now() + timedelta(seconds=auth_response['expires_in']))

        OAuthCredentials.objects.create(
            user=request.user,
            service='stripe',
            access_token=auth_response['access_token'],
            refresh_token=auth_response['refresh_token'],
            expiration_at=timezone.now() + timedelta(seconds=auth_response['expires_in'])
        )
    except Exception as e:
        logging.error(f"Exception in handling Stripe callback: {str(e)}")
        return redirect('profile')  # Redirect to an error handling page or similar

    return redirect('integrations')

@login_required
def datadog_auth(request):
    state_token = get_CSRF_token(request)
    request.session['auth_state'] = state_token
    params = {
        'client_id': settings.DATADOG_CLIENT_ID,
        'redirect_uri': settings.DATADOG_REDIRECT_URI,
        'response_type': 'code',
        'state': state_token
    }
    url = f"https://app.datadoghq.com/oauth2/v1/authorize?{urlencode(params)}"
    print("Redirecting to URL:", url)  # Print the URL to debug
    return redirect(url)

@login_required
def datadog_callback(request):
    auth_code = request.GET.get('code')
    state_token = request.session.get('auth_state')
    received_state = request.GET.get('state')

    if not state_token or state_token != received_state:
        logging.error("Invalid state token")
        return redirect('profile')  # Redirect to an error handling page

    token_url = 'https://app.datadoghq.com/oauth2/v1/authorize'
    print("auth_code:", auth_code)
    try:
        auth_response = requests.post(token_url, data={
            'grant_type': 'authorization_code',
            'client_id': settings.DATADOG_CLIENT_ID,
            'client_secret': settings.DATADOG_CLIENT_SECRET,
            'redirect_uri': settings.DATADOG_REDIRECT_URI,
            'code': auth_code
        }, headers={'Content-Type': 'application/x-www-form-urlencoded'}).json()

        if 'error' in auth_response:
            logging.error(f"Error from Datadog: {auth_response['error']}")
            return redirect('profile')  # Redirect to an error handling page or similar

        print("Datadog access token", auth_response['access_token'], "created.")
        print("Expires:", timezone.now() + timedelta(seconds=auth_response['expires_in']))

        OAuthCredentials.objects.create(
            user=request.user,
            service='datadog',
            access_token=auth_response['access_token'],
            refresh_token=auth_response['refresh_token'],
            expiration_at=timezone.now() + timedelta(seconds=auth_response['expires_in'])
        )
    except Exception as e:
        logging.error(f"Exception in handling HubSpot callback: {str(e)}")
        return redirect('profile')  # Redirect to an error handling page or similar

    return redirect('integrations')

