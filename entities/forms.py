from django import forms
from .models import mmCompanies

class CompanyForm(forms.ModelForm):
    class Meta:
        model = mmCompanies
        fields = ['name', 'city', 'state', 'country', 'sector','size']
