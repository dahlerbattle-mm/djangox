from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, CustomUser
from .forms import ProfileForm
from entities.forms import CompanyForm
from entities.models import mmCompanies
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.models import User

@login_required
def profile_view(request):
    # Get or create the profile linked to the current user
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Check if the current user is already linked to a company
    company_query = mmCompanies.objects.filter(users__in=[request.user])
    company = company_query.first() if company_query.exists() else mmCompanies()

    if request.method == 'POST':
        # Use Django's transaction.atomic to ensure data integrity
        with transaction.atomic():
            profile_form = ProfileForm(request.POST, instance=profile, prefix='profile')
            company_form = CompanyForm(request.POST, instance=company, prefix='company')

            if profile_form.is_valid() and company_form.is_valid():
                profile_form.save()
                saved_company = company_form.save(commit=False)
                if not company_query.exists():
                    saved_company.save()
                    # saved_company.users.add(request.CustomUser)  # Add user to the new company

                return redirect('home')  # Redirect to the 'home' page on success

    else:
        profile_form = ProfileForm(instance=profile, prefix='profile')
        company_form = CompanyForm(instance=company, prefix='company')

    context = {
        'profile_form': profile_form,
        'company_form': company_form
    }
    
    return render(request, 'account/profile.html', context)
