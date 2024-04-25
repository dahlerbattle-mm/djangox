from django.shortcuts import render, redirect
from django.utils.timezone import now
from accounts.forms import ProfileForm
from .forms import CompanyForm
from .models import mmCompanies
import uuid

def edit_profile(request):
    try:
        company = mmCompanies.objects.get(users=request.user)
        form = CompanyForm(instance=company)
    except mmCompanies.DoesNotExist:
        form = CompanyForm()

    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company if 'company' in locals() else None)
        if form.is_valid():
            company = form.save(commit=False)
            if not company.mmc_id:  # Check if mmc_id is not already set
                company.mmc_id = str(uuid.uuid4())  # Generate a unique ID
            company.updated_at = now()  # Auto-set the update time
            if not company.created_at:  # Check if created_at is not already set
                company.created_at = now()  # Auto-set the creation time
            company.save()
            company.users.add(request.user)  # Add the current user to the users list
            email_domain = request.user.email.split('@')[1]
            company.url = f'http://{email_domain}'
            company.save()

            return redirect('profile_updated')  # Redirect to a new URL on success
    return render(request, 'account/profile.html', {'form': form})
