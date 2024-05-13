from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.http import JsonResponse

from .models import DashboardData
from .utilities import extract_domain_from_email, get_customer_info
from entities.models import add_global_company, GlobalCompanies
from entities.utilities import generate_random_number

import json
import numpy as np

# class RevenuePageView(TemplateView):
#     template_name = "dashboards/revenue.html"

def revenue_view(request):
    metrics = settings.REVENUE_CATEGORIES
    return render(request, 'dashboards/revenue.html', {'metrics': metrics})

def cashflow_view(request):
    metrics = settings.CASHFLOW_CATEGORIES
    return render(request, 'dashboards/cashflow.html', {'metrics': metrics})

def summary_view(request):
    metrics = settings.SUMMARY_CATEGORIES
    return render(request, 'dashboards/summary.html', {'metrics': metrics})

# class ExpensesPageView(TemplateView):
#     template_name = "dashboards/expenses.html"

def expenses_view(request):
    metrics = settings.EXPENSES_CATEGORIES
    return render(request, 'dashboards/expenses.html', {'metrics': metrics})

# class FinancialsPageView(TemplateView):
#     template_name = "dashboards/financials.html"

def financials_view(request):
    metrics = settings.FINANCIAL_CATEGORIES
    return render(request, 'dashboards/financials.html', {'metrics': metrics})

# class SaaSMetricsPageView(TemplateView):
#     template_name = "dashboards/saas_metrics.html"

def saas_view(request):
    metrics = settings.SAAS_METRICS_CATEGORIES
    return render(request, 'dashboards/saas_metrics.html', {'metrics': metrics})

# class ServicesPageView(TemplateView):
#     template_name = "dashboards/services.html"

def services_view(request):
    metrics = settings.SERVICES_CATEGORIES
    return render(request, 'dashboards/services.html', {'metrics': metrics})

# class PipelinePageView(TemplateView):
#     template_name = "dashboards/pipeline.html"

def pipeline_view(request):
    metrics = settings.PIPELINE_CATEGORIES
    return render(request, 'dashboards/pipeline.html', {'metrics': metrics})

def product_view(request):
    metrics = settings.PRODUCT_CATEGORIES
    return render(request, 'dashboards/product.html', {'metrics': metrics})

def hr_view(request):
    metrics = settings.HR_CATEGORIES
    return render(request, 'dashboards/hr.html', {'metrics': metrics})


def qb_revenue_clean(request): 
    """Cleans raw revenue json for final output in the Revenue Dashboard"""
    # Fetch QuickBooks credentials
    qb_object = DashboardData.objects.get(user=request.user, source='quickbooks', category='revenue')
    payload = qb_object.payload.get('QueryResponse', {}).get('Invoice', [])

    clean_payload = []
    revenues = []

    for txn in payload: 
        txn_id = txn.get('Id', "Unkown") #.get('City', "Unkown"),
        txn_date =  txn.get('TxnDate', "Unknown")
        amount = txn.get('TotalAmt', "0")
        revenues.append(float(amount))

        customer = txn.get('CustomerRef', "Unknown").get('name', "Unkown")
        email = txn.get('BillEmail', "Unknown").get('Address', "Unkown")
        url = extract_domain_from_email(email)

        #gets additional customer details inccluding location, size, and sector
        customer_details = get_customer_info(customer, url, txn)

        txn_dict = {
            'txn_id' : txn_id,
            'date' : txn_date, 
            'amount' : amount, 
            'customer' : customer, 
            'customer_url' : url, 
            'customer_city' : customer_details.get('city', 'Unknown'),
            'customer_state' : customer_details.get('state', 'Unknown'),
            'customer_country' : customer_details.get('country', 'Unknown'),
            'customer_size' : customer_details.get('size', 'Unknown'),
            'customer_sector' : customer_details.get('sector', 'Unknown'),
            'customer_pandl_category' : customer_details.get('p_and_l_category', 'Unknown'),
            'customer_pandl_subcategory' : customer_details.get('p_and_l_subcategory', 'Unknown'),
            'relationship_type' : None, 
            'product_type' : None, 
        }
        # Append to clean payload
        clean_payload.append(txn_dict)

    bottom_third_revenue - np.percentile(revenues, 33.33)
    top_third_revenue = np.percentile(revenues, 66.66)

    #puts revenues into product/service categories based on price
    for txn in clean_payload:
        if txn.amount >= top_third_revenue: 
            txn.product_type = "upper_tier"
        elif txn.amount < bottom_third_revenue: 
            txn.product_type = "lower_tier"
        else: 
            txn.product_type = "middle_tier"

    qb_object.clean_payload = clean_payload
    qb_object.save()
    
    return JsonResponse(clean_payload, safe=False)


def qb_expenses_clean(request): 
    """Cleans raw expenses json for final output in the Expenses Dashboard"""
    # Fetch QuickBooks credentials
    qb_object = DashboardData.objects.get(user=request.user, source='quickbooks', category='expenses')
    payload = qb_object.payload.get('QueryResponse', {}).get('Purchase', [])

    clean_payload = []

    for txn in payload: 
        #get first line txn items 
        txn_id = txn.get('Id', "Unkown") 
        txn_date =  txn.get('TxnDate', "Unknown")
        amount = txn.get('TotalAmt', "0")

        # Check if EntityRef exists and is a dictionary before attempting to access 'name'
        entity_ref = txn.get('EntityRef', {})
        vendor = entity_ref.get('name', "Unknown") if isinstance(entity_ref, dict) else "Unknown"
        url = "unknown.com"

        pandl_category = txn.get('Line', {})[0].get('DetailType')
        # Assuming txn is your transaction dictionary that contains the 'Line' key
        pandl_subcategory = txn.get('Line', [{}])[0].get('AccountBasedExpenseLineDetail', {}).get('AccountRef', {}).get('name', 'Unknown')

        # company = GlobalCompanies.objects.get(gc_id=company_id)


        #gets additional customer details inccluding location, size, and sector
        vendor_details = get_customer_info(vendor, url, txn)

        txn_dict = {
            'txn_id' : txn_id,
            'date' : txn_date, 
            'amount' : amount, 
            'vendor' : vendor, 
            'customer_url' : url, 
            'customer_city' : vendor_details.get('city', 'Unknown'),
            'customer_state' : vendor_details.get('state', 'Unknown'),
            'customer_country' : vendor_details.get('country', 'Unknown'),
            'customer_size' : vendor_details.get('size', 'Unknown'),
            'customer_sector' : vendor_details.get('sector', 'Unknown'),
            'customer_pandl_category' : pandl_category,
            'customer_pandl_subcategory' : pandl_subcategory,
        }
        # Append to clean payload
        clean_payload.append(txn_dict)

    qb_object.clean_payload = clean_payload
    qb_object.save()

    return JsonResponse(clean_payload, safe=False)