from django.contrib import admin
from .models import mmCompanies
from .forms import CompanyForm

# Profile admin interface
class mmCompaniesAdmin(admin.ModelAdmin):
    # add_form = N/A
    form = CompanyForm
    model = mmCompanies
    list_display = ['mmc_id', 'name', 'url', 'created_at', 'updated_at']

# Register the admin class with the associated model
admin.site.register(mmCompanies, mmCompaniesAdmin)
