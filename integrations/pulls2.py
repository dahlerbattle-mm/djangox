from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils import timezone

from .models import OAuthCredentials
from dashboards.models import DashboardData

from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from dateutil import parser
from datetime import datetime
import json

@login_required
def fetch_quickbooks_data(request):
    """Fetches raw quickbooks JSON data and stores it in the DashboardData model"""
    try:
        # Fetch QuickBooks credentials
        credentials = OAuthCredentials.objects.get(user=request.user, service='quickbooks')

        # Determine date range for the queries
        if credentials.last_api_pull_at:
            start_date = credentials.last_api_pull_at
        else:
            start_date = timezone.now() - datetime.timedelta(days=2*365)  # Two years ago

        start_date = parser.parse(str(start_date))
        start_date = start_date.strftime('%Y-%m-%d')

        end_date = timezone.now()
        end_date = parser.parse(str(end_date))
        end_date = end_date.strftime('%Y-%m-%d')

        print("Start Date:", start_date)
        print("End Date:", end_date)

        # Initialize the AuthClient
        auth_client = AuthClient(
            client_id=settings.QUICKBOOKS_CLIENT_ID,
            client_secret=settings.QUICKBOOKS_CLIENT_SECRET,
            environment='sandbox',  # Or 'production'
            redirect_uri=settings.QUICKBOOKS_REDIRECT_URI,
        )

        # Use the stored tokens and check if the access token has expired
        auth_client.access_token = credentials.access_token
        auth_client.refresh_token = credentials.refresh_token

        if timezone.now() >= credentials.expiration_at:
            auth_client.refresh()  # Refresh the token using the AuthClient

            # Update the stored credentials
            credentials.access_token = auth_client.access_token
            credentials.refresh_token = auth_client.refresh_token
            credentials.expiration_at = timezone.now() + timezone.timedelta(seconds=auth_client.expires_in)
            credentials.save()

        # Setup the QuickBooks client using the AuthClient instance
        qb_client = QuickBooks(
            auth_client=auth_client,
            company_id=credentials.realm_id
        )

        try: 
            #NOTE: Still need to insert parameters by date
            revenue = qb_client.query("SELECT * FROM Invoice")# WHERE TxnDate >= '{start_date}' AND TxnDate <= '{end_date}'")
            expenses = qb_client.query("SELECT * FROM Purchase")# WHERE TxnDate >= '{start_date}' AND TxnDate <= '{end_date}'")
            customers = qb_client.query("SELECT * FROM Customer ORDERBY FamilyName")
            profit_loss = qb_client.get_report("ProfitAndLoss")#, start_date=start_date, end_date=end_date)
            bs = qb_client.get_report("BalanceSheet")#, as_of_date=end_date)
        except Exception as e:
            print(f"Error fetching Quickbook Queries: {str(e)}")

        # Update last_api_pull_at
        credentials.last_api_pull_at = timezone.now()
        credentials.save()

        # Assuming the results are already in a JSON-parsable format
        results = {
            "revenue": revenue,
            "expenses": expenses,
            "customers": customers,
            "p&l": profit_loss,
            "balance_sheet": bs
        }


        # Load each item into DashboardData
        for key, data in results.items():
            category = key
            if category:  # Ensure the category is defined
                DashboardData.objects.create(
                    user=request.user,
                    source="quickbooks",
                    category=category,
                    payload=data,
                    clean_payload=None,  # or some cleaning process if required
                    created_at=timezone.now(),
                    updated_at=None  # explicitly set to None
                )

        return JsonResponse(results)

    except OAuthCredentials.DoesNotExist:
        return HttpResponse("No QuickBooks credentials found for this user.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
