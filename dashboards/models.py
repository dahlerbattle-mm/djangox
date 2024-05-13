from django.db import models
from django.conf import settings
#from entities.models import mmCompanies

# DATA_CATEGORIES = (
#     ('revenue', 'Revenue'),
#     ('expenses', 'Expenses'),
#     ('p&l', 'P&L'),
#     ('balance_sheet', 'Balance Sheet'),
#     ('customers', 'Customers'),
#     ('deals', 'Deals'),
#     ('product', 'Product'),
#     ('services', 'Services'),
#     ('hr', 'HR'),
# )

# SOURCE_CATEGORIES = (
#     ('quickbooks', 'Quickbooks'),
#     ('hubspot', 'HubSpot'),
#     ('stripe', 'Stripe'),
#     ('jira', 'Jira'),
#     ('datadog', 'Datadog'),
# )

class DashboardData(models.Model):
    """A centralized repository of JSON-based information used in the final dashboards."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #company = models.ForeignKey(mmCompanies.name, on_delete=models.CASCADE)
    source = models.CharField(max_length=30, null=True, blank=True)
    category = models.CharField(max_length=30, null=True, blank=True)
    payload = models.JSONField()
    clean_payload = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @property
    def company(self):
        return self.user.company

    def __str__(self):
        return f"{self.user}'s {self.category}"