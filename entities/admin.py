from django.contrib import admin
from .models import mmCompanies, GlobalCompanies
from .forms import CompanyForm

# Profile admin interface
class mmCompaniesAdmin(admin.ModelAdmin):
    """Admin view for the MetricMatters customers (mmCompanies)"""
    # add_form = N/A
    form = CompanyForm
    model = mmCompanies
    list_display = ['mmc_id', 'name', 'url', 'city', 'state', 'country', 'size', 'sector', 'created_at', 'updated_at']

# Register the admin class with the associated model
admin.site.register(mmCompanies, mmCompaniesAdmin)

# Profile admin interface
class GlobalCompaniesAdmin(admin.ModelAdmin):
    """Admin view for mmCompany's customers and vendors"""
    # add_form = N/A
    # form = CompanyForm
    model = GlobalCompanies
    list_display = ['gc_id', 'name', 'url', 'city', 'state', 'country', 'size', 'sector', 'created_at', 'updated_at']

# Register the admin class with the associated model
admin.site.register(GlobalCompanies, GlobalCompaniesAdmin)
