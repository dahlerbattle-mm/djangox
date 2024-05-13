from django.urls import path
from . import views
from . import pulls2
from dashboards.views import qb_expenses_clean

urlpatterns = [
    path("", views.index, name="integrations"),
    path('connect/quickbooks/', views.quickbooks_auth2, name='quickbooks_connect'),
    path('callback/quickbooks/', views.quickbooks_callback2, name='quickbooks_callback'),
    path('fetch/quickbooks/', pulls2.fetch_quickbooks_data, name='quickbooks_fetch'),
    path('connect/hubspot/', views.hubspot_auth, name='hubspot_connect'),
    path('callback/hubspot/', views.hubspot_callback2, name='hubspot_callback'),
    path('connect/stripe/', views.stripe_auth, name='stripe_connect'),
    path('callback/stripe/', views.stripe_callback, name='stripe_callback'),
    path('connect/jira/', views.jira_auth, name='jira_connect'),
    path('callback/jira/', views.jira_callback, name='jira_callback'),
    path('connect/datadog/', views.datadog_auth, name='datadog_connect'),
    path('callback/datadog/', views.datadog_callback, name='datadog_callback'),
    path('connect/salesforce/', views.hubspot_auth, name='salesforce_connect'),
    path('connect/xero/', views.hubspot_auth, name='xero_connect'),
    path('connect/mailchimp/', views.hubspot_auth, name='mailchimp_connect'),
    path('connect/zoho/', views.hubspot_auth, name='zoho_connect'),
    path('connect/activecampaign/', views.hubspot_auth, name='activecampaign_connect'),
    path('connect/freshbooks/', views.hubspot_auth, name='freshbooks_connect'),
    path('connect/sage/', views.hubspot_auth, name='sage_connect'),
    path('connect/mondaydotcom/', qb_expenses_clean, name='mondaydotcom_connect'),
]