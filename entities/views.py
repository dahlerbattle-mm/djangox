from django.shortcuts import render, redirect
from django.utils.timezone import now
from .forms import CompanyForm
from .models import mmCompanies
import random

# Ensure your `generate_random_number` function is correctly generating a unique number as needed.
def generate_random_number():
    return random.randint(100000, 999999)

def edit_profile(request):
    # Initialize `company` to None
    company = None

    # Use `get_or_create` which will return a tuple (object, created), so unpack accordingly
    company, created = mmCompanies.objects.get_or_create(users=request.user)
    
    # Pass the `company` instance to the form
    form = CompanyForm(instance=company)

    if request.method == 'POST':
        # Pass the POST data and the `company` instance to the form
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            # Save the form with `commit=False` to get the company object without committing to the DB
            company = form.save(commit=False)

            # Only set `mmc_id` if it's not already set, and update timestamps
            if not company.mmc_id:
                company.mmc_id = "mmc_id_" + str(generate_random_number())

            company.updated_at = now()  # Always update the 'updated_at' timestamp
            if not company.created_at:
                company.created_at = now()  # Set 'created_at' only if not set

            # Derive the company URL from the user's email
            email_domain = request.user.email.split('@')[1]
            company.url = f'http://{email_domain}'
            print(company.url)

            # Save the company instance to the database
            company.save()

            # If this is a new company, add the user
            if created:
                company.users.add(request.user)

            # Redirect to the profile updated page
            return redirect('profile_updated')
    
    # Render the profile editing form
    return render(request, 'account/profile.html', {'form': form})
