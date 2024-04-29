from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="integrations"),
    path('connect/quickbooks/', views.quickbooks_auth, name='quickbooks_connect'),
    path('callback/quickbooks/', views.quickbooks_callback, name='quickbooks_callback'),
    path('connect/hubspot/', views.connect_to_qb, name='hubspot_connect'),
    path('connect/stripe/', views.connect_to_qb, name='stripe_connect'),
    path('connect/jira/', views.connect_to_qb, name='jira_connect'),
    path('connect/salesforce/', views.connect_to_qb, name='salesforce_connect'),
    path('connect/xero/', views.connect_to_qb, name='xero_connect'),
    path('connect/mailchimp/', views.connect_to_qb, name='mailchimp_connect'),
    path('connect/zoho/', views.connect_to_qb, name='zoho_connect'),
    path('connect/activecampaign/', views.connect_to_qb, name='activecampaign_connect'),
    path('connect/freshbooks/', views.connect_to_qb, name='freshbooks_connect'),
    path('connect/sage/', views.connect_to_qb, name='sage_connect'),
    path('connect/mondaydotcom/', views.connect_to_qb, name='mondaydotcom_connect'),

    # path("success/", views.integration_success, name="success"),
    # path("quickbooks/redirect/", views.qb_auth_code_handler, name="redirect_quickbooks"),
    # path("quickbooks/connect/", views.connect_to_qb, name="connect_quickbooks"),
    # path("quickbooks/", views.quickbooks_integration, name="new_quickbooks"),
]