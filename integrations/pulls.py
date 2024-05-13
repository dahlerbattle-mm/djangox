from django.utils import timezone
from django.db import IntegrityError
from datetime import timedelta
import requests
from entities.models import generate_random_gc_id, add_global_company, GlobalCompanies

def fetch_expenses(credential, url=url, headers=headers, start_date=start_date, end_date=end_date):
    # Define the query to fetch Expense transactions
    query = f"""
    SELECT * FROM Purchase WHERE TxnDate >= '{start_date}' AND TxnDate <= '{end_date}' ORDER BY TxnDate DESC
    """
    payload = {'query': query}
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        expenses = response.json()
        # Create a DashboardData entry
        DashboardData.objects.create(
            user=credential.user,
            company=credential.user,  # Assuming user has a company attribute
            source='quickbooks',
            category='expenses',
            payload=expenses,
            clean_payload=None,
            updated_at=datetime.now()
        )
        return expenses
    else:
        print(f"Failed to fetch expenses: {response.status_code}, {response.text}")
        return None

def fetch_revenue(credential, url=url, headers=headers, start_date=start_date, end_date=end_date):
    # Define the query to fetch Expense transactions
    query = f"""
    SELECT * FROM Invoice WHERE TxnDate >= '{start_date}' AND TxnDate <= '{end_date}' ORDER BY TxnDate DESC
    """
    payload = {'query': query}
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        revenues = response.json()
        # Create a DashboardData entry
        DashboardData.objects.create(
            user=credential.user,
            company=credential.user,  # Assuming user has a company attribute
            source='quickbooks',
            category='expenses',
            payload=revenues,
            clean_payload=None,
            updated_at=datetime.now()
        )
        return expenses
    else:
        print(f"Failed to fetch invoices: {response.status_code}, {response.text}")
        return None

def fetch_financials(credential, url=url, headers=headers, start_date=start_date, end_date=end_date):
    daily_reports = []

    while current_date <= end_date:
        # Fetch the Profit and Loss report for the current date
        profit_and_loss_url = f"{url}/ProfitAndLoss?start_date={start_date}&end_date={end_date}"
        pl_response = requests.get(profit_and_loss_url, headers=headers)

        # Fetch the Balance Sheet report for the current date
        balance_sheet_url = f"{url}/BalanceSheet?as_of_date={date_str}"
        bs_response = requests.get(balance_sheet_url, headers=headers)

        # Check responses and collect data
        if pl_response.status_code == 200 and bs_response.status_code == 200:
            pl_data = pl_response.json()
            bs_data = bs_response.json()
            daily_reports.append({
                'date': date_str,
                'profit_and_loss': pl_data,
                'balance_sheet': bs_data
            })

            # Create a DashboardData entry
            DashboardData.objects.create(
                user=credential.user,
                company=credential.user,
                source='quickbooks',
                category='financials',
                payload=daily_reports,
                clean_payload=None,
                updated_at=datetime.now()
            )
        else:
            print(f"Failed to fetch reports for {date_str}: P&L status {pl_response.status_code}, BS status {bs_response.status_code}")

        # Move to the next day
        current_date += timedelta(days=1)

def fetch_hubspot_companies(headers=headers, start_date=start_date, end_date=end_date):
    all_companies = []
    url = "https://api.hubapi.com/crm/v3/objects/companies"
    params = {
        "limit": 250,  # Fetch up to 250 companies at a time, adjust as necessary
        "properties": "name,domain,city,'state',country,annual_revenue,industry,website_url,createdate"  # Specify additional properties if needed
    }

    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch companies: {response.status_code}")
            break
        
        data = response.json()
        all_companies.extend(data['results'])

        # HubSpot uses paging with "next" links to manage large sets of data
        url = data['paging']['next']['link'] if 'paging' in data and 'next' in data['paging'] else None

    # Check if each company already exists in the GlobalCompanies model by its website
        for company in data['results']:
            url = company['properties'].get('domain') or company['properties'].get('website')
            if not GlobalCompanies.objects.filter(url=url).exists():
                try:
                    GlobalCompanies.objects.create(
                        gc_id=generate_random_gc_id(),
                        name=company['properties'].get('name', ''),
                        url=url,
                        mm_Companies=credential.user,
                        image=null,
                        city=company['properties'].get('city', ''),
                        state=company['properties'].get('state/region', ''),
                        country=company['properties'].get('country', ''),
                        size=company['properties'].get('annual_revenue', ''),
                        sector=company['properties'].get('industry', ''),
                        created_at=company['properties'].get('createdate', ''),
                        updated_at=company['properties'].get('createdate', '')
                    )
                    print(f"Added {company['properties'].get('name', '')} to database.")
                except IntegrityError as e:
                    print(f"Could not add {company['properties'].get('name', '')}: {e}")

def fetch_quickbooks_companies(url=url, headers=headers):

    url = f"https://api.hubapi.com/crm/v3/objects/companies"

    query = """
    SELECT DisplayName, PrimaryEmailAddr.Address as Email, BillAddr.City, BillAddr.Country, BillAddr.Line1, 
           BillAddr.PostalCode, BillAddr.Region, MetaData.CreateTime, CustomField 
    FROM Customer
    """
    payload = {'query': query}
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        customers = response.json().get('QueryResponse', {}).get('Customer', [])
        for customer in customers:
            # Assuming CustomField contains a field for URL, Industry, and Annual Revenue
            url = next((field['StringValue'] for field in customer.get('CustomField', []) if field['Name'] == 'URL'), None)
            if url and not GlobalCompanies.objects.filter(url=url).exists():
                try:
                    GlobalCompanies.objects.create(
                        gc_id=generate_random_gc_id(),
                        name=customer.get('DisplayName', ''),
                        url=url,
                        # Assuming you handle the user and related fields differently
                        image=None,
                        city=customer.get('BillAddr', {}).get('City', ''),
                        state=customer.get('BillAddr', {}).get('Region', ''),
                        country=customer.get('BillAddr', {}).get('Country', ''),
                        size=next((field['StringValue'] for field in customer.get('CustomField', []) if field['Name'] == 'Annual Revenue'), ''),
                        sector=next((field['StringValue'] for field in customer.get('CustomField', []) if field['Name'] == 'Industry'), ''),
                        created_at=customer.get('MetaData', {}).get('CreateTime'),
                        updated_at=customer.get('MetaData', {}).get('CreateTime')
                    )
                    print(f"Added {customer.get('DisplayName', '')} to GlobalCompanies.")
                except IntegrityError as e:
                    print(f"Could not add {customer.get('DisplayName', '')}: {e}")
    else:
        print(f"Failed to fetch customers: {response.status_code}")

def fetch_hubspot_deals(headers=headers):
    all_deals = []
    url = f"https://api.hubapi.com/crm/v3/objects/deals"
    params = {
        "limit": 100,  # Adjust based on how many deals you expect to fetch at a time
        "properties": "dealname,dealstage,closedate,amount,dealtype",  # Specify the properties you need
        "paginate": "true"  # HubSpot handles pagination with 'after' cursor
    }
    
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            all_deals.extend(data.get('results', []))
            # Check if there's a next page
            paging = data.get('paging', {})
            next_page = paging.get('next', {})
            url = next_page.get('link') if next_page else None
            # Update params to include the cursor for the next page
            if next_page:
                params['after'] = next_page.get('after')

            # Create a DashboardData entry
            DashboardData.objects.create(
                user=credential.user,
                company=credential.user,  # Assuming user has a company attribute
                source='hubspot',
                category='deals',
                payload=all_deals,
                clean_payload=None,
                updated_at=datetime.now()
            )

        else:
            print(f"Failed to fetch deals: {response.status_code}, {response.text}")



def update_dashboard_data():
    credentials = OAuthCredentials.objects.all()
    for credential in credentials:
        start_date = credential.last_api_pull_at
        if start_date is None:
            start_date = timezone.now() - timedelta(days=2*365)  # Two years ago
        
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')

        if credential.service == "quickbooks": 
            url = f"https://quickbooks.api.intuit.com/v3/company/{credential.realm_id}/query"
            headers = {
                'Authorization': f'Bearer {credential.access_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/text'
            }
            
            fetch_expenses(credential, url=url, headers=headers, start_date=start_date, end_date=end_date)
            fetch_revenue(credential, url=url, headers=headers, start_date=start_date, end_date=end_date)
            fetch_financials(credential, url=url, headers=headers, start_date=start_date, end_date=end_date)
            fetch_quickbooks_companies(url=url, headers=headers)


        elif credential.service == "hubspot": 
            headers = {
                "Authorization": f"Bearer {credential.access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            fetch_hubspot_companies(headers=headers, start_date=start_date, end_date=end_date)
            fetch_hubspot_deals(headers=headers)

        elif credential.service == "stripe": 
            print("stripe)")

        else: 
            continue 

