from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.http import JsonResponse

from .forms import CompanyForm
from .models import GlobalCompanies, generate_random_gc_id, in_global_companies
from .utilities import generate_random_number, get_domain, currency_to_country
from dashboards.models import DashboardData

import tldextract
import random


def edit_profile(request):
    """Generates a mmCompanies profile"""
    # Initialize `company` to None
    company = None

    # Use `get_or_create` which will return a tuple (object, created), so unpack accordingly
    company, created = mmCompanies.objects.get_or_create(users=request.user)
    
    # Pass the `company` instance to the form
    form = CompanyForm(instance=company)

    if request.method == 'POST':
        # Pass the POST data and the `company` instance to the form
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            # Save the form with `commit=False` to get the company object without committing to the DB
            company = form.save(commit=False)

            # Only set `mmc_id` if it's not already set, and update timestamps
            if not company.mmc_id:
                company.mmc_id = "mmc_id_" + str(generate_random_number())

            company.updated_at = now()  # Always update the 'updated_at' timestamp
            if not company.created_at:
                company.created_at = now()  # Set 'created_at' only if not set

            # Derive the company URL from the user's email
            email_domain = request.user.email.split('@')[1]
            company.url = f'http://{email_domain}'
            print(company.url)

            # Save the company instance to the database
            company.save()

            # If this is a new company, add the user
            if created:
                company.users.add(request.user)

            # Redirect to the profile updated page
            return redirect('profile_updated')
    
    # Render the profile editing form
    return render(request, 'account/profile.html', {'form': form})


def quickbooks_clean(request): 
    """Cleans QUickbooks information"""
    # Fetch QuickBooks credentials
    qb_object = DashboardData.objects.get(user=request.user, source='quickbooks', category='customers')

    # Safe access to 'QueryResponse' and then to 'Customer'
    customers = qb_object.payload.get('QueryResponse', {}).get('Customer', [])

    # Iterate over each customer in the list
    for customer in customers:
        # Use get to safely access keys
        name = customer.get('CompanyName', customer.get('DisplayName', 'Unknown Name'))
        url = customer.get('WebAddr', {}).get('URI', "www.unknown.com")
        url = get_domain(url)
        currency = customer.get('CurrencyRef', None).get('name', None)
        country = currency_to_country(currency)

        # Ensure that you replace `in_global_companies` and `generate_random_gc_id` with your actual implementations
        if not in_global_companies(name, url) and url != "unknown.com":
            new_company = GlobalCompanies.objects.create(
                gc_id = generate_random_gc_id(),
                name = name,
                url = url,
                image = None,
                city = customer.get('BillAddr', "Unkown").get('City', "Unkown"),
                state = customer.get('BillAddr', "Unkown").get('City', "CountrySubDivisionCode"),
                country = country,
                size = "Unknown",
                sector = "Unknown",
            )

            # # Properly manage many-to-many relationship
            # FIX THIS!
            # new_company.mm_Companies.add([request.user.id])

            print("Company", name, "added to Global Companies")
        else: 
            print("Company", name, "not added to Global Companies")
  

    # return JsonResponse(customers, safe=False)
    
    
