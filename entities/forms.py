from django import forms
from .models import mmCompanies

class CompanyForm(forms.ModelForm):
    """Form used when filling out the user profile to savve the user's company details"""
    class Meta:
        model = mmCompanies
        fields = ['name', 'city', 'state', 'country', 'sector','size']
