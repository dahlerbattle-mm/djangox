from django.db import models
from django.conf import settings
from accounts.models import CustomUser
from dashboards.models import DashboardData
from django.contrib.postgres.fields import ArrayField
import random

SIZE_CHOICES = (
        ('SME', '1-9'),
        ('SME', '10-49'),
        ('Lower Middle Market', '50-99'),
        ('Upper Middle Market', '100+')
    )

SECTOR_CHOICES = (
        ('information_technology', 'Information Technology'), 
        ('consumer_discretionary', 'Consumer Discretionary'),
        ('communication_services', 'Communication Services'),
        ('unknown', 'Unknown'),
        ('financials', 'Financials'),
        ('healthcare', 'Healthcare'),
        ('energy', 'Energy'),
        ('consumer_staples', 'Consumer Staples'),
        ('materials', 'Materials'),
        ('industrials', 'Industrials'),
        ('utilities', 'Utilities'),
        ('real_estate', 'Real Estate'), 
    )

P_AND_L_CATEGORY_CHOICES = (
        ('revenue', 'Revenue'), 
        ('cogs', 'COGS'), 
        ('g&a', 'G&A'),
        ('s&m', 'S&M'),
        ('d&a', 'D&A'),
        ('r&d', 'R&D'),
        ('interest', 'Interest'),
        ('non_operating_income', 'Non Operating Income'),
        ('non_operating_expense', 'Non Operating Expense'),
        ('taxes', 'Taxes'),
    )

P_AND_L_SUBCATEGORY_CHOICES = (
        ('product_income', 'Product Income'), 
        ('service_income', 'Service Income'),
        ('subscription_income', 'Subscription Income'),
        ('royalty_income', 'Royalty Income'),
        ('other_income', 'Other Income'),
        ('materials', 'COGS - Materials'),
        ('direct_labor', 'COGS - Direct Labor'),
        ('manufacturing_supplies', 'COGS - Manufacturing Supplies'),
        ('production_overhead', 'COGS - Production Overhead'),
        ('office', 'G&A - Office'),
        ('g&a_salaries', 'G&A - Salaries'),
        ('rent_lease', 'G&A - Rent & Lease'),
        ('utilities', 'G&A - Utilities'),
        ('misc.', 'G&A - Misc.'),
        ('r&d_salaries.', 'R&D - Salaries'),
        ('product_development', 'R&D - Product Development'),
        ('software_development', 'R&D - Software Development'),
        ('s&m_salaries', 'S&M - Salaries'),
        ('s&m_software', 'S&M - Software'),
        ('s&m_advertising', 'S&M - Advertising'),
        ('s&m_commisions', 'S&M - Commisions'),
        ('county_taxes', 'Taxes - County'),
        ('state_taxes', 'Taxes - State'),
        ('federal_taxes', 'Taxes - Federal'),
        ('sale_of_assets', 'Non-Operating - Sale of Asset Gain/Loss'),
        ('fx_gain_loss', 'Non-Operating - Foreign Exchange Gain/Loss'),
        ('investment_income', 'Non-Operating - Investment Income Gain/Loss'),
        ('grant', 'Non-Operating - Grant Income'),
    )

# mmCompanies Model
class mmCompanies(models.Model):
    """Saves a user's company information"""
    # Relationship to User model
    mmc_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=200, blank=True, null=True)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    size = models.CharField(max_length=100, choices=SIZE_CHOICES)
    sector = models.CharField(max_length=100, choices=SECTOR_CHOICES)
    s3_url = models.URLField(max_length=200, blank=True, null=True)
    low_tier_price = models.IntegerField(blank=True, null=True)
    mid_tier_price = models.IntegerField(blank=True, null=True)
    upper_tier_price = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.mmc_id:  # Generate profile_id only if it's not already set
            self.mmc_id = self._generate_unique_mmc_id()
            
        if self.users_id and not self.url:  # Check if there's a related user and no URL set yet
            user_model = models.get_model(*settings.AUTH_USER_MODEL.split('.'))
            user_instance = user_model.objects.get(id=self.users_id)
            email_domain = user_instance.email.split('@')[1]
            self.url = f'http://{email_domain}'  # Set the URL based on the user's email

        super(mmCompanies, self).save(*args, **kwargs)
    
    def _generate_unique_mmc_id(self):
        while True:
            potential_id = "mmc_id" + str(random.randint(100000, 999999))  # Generate a random number between 100000 and 999999
            if not mmCompanies.objects.filter(mmc_id=potential_id).exists():
                return potential_id

    def __str__(self):
        return self.name

from django.db import models

# GlobalCompanies Model
class GlobalCompanies(models.Model):
    gc_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=200, blank=True, null=True)
    mm_Companies = models.ManyToManyField(mmCompanies, related_name='mm_companies')
    image = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True) #choices=SIZE_CHOICES
    sector = models.CharField(max_length=100, blank=True, null=True)  #choices=SIZE_CHOICES
    p_and_l_category = ArrayField(models.CharField(max_length=100, choices=P_AND_L_CATEGORY_CHOICES), default=list, blank=True)
    p_and_l_subcategory = ArrayField(models.CharField(max_length=100, choices=P_AND_L_SUBCATEGORY_CHOICES), default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def generate_random_gc_id():
    return "gc_id_" + str(random.randint(100000, 999999))

def in_global_companies(name, url):
    return GlobalCompanies.objects.filter(url=url, name=name).exists()

def add_global_company(name, url=None, mm_companies=None, image=None, city=None, state=None, country=None, company_size=None, sector=None, mm_company_list=None):
    """Create and save a new GlobalCompany instance with various optional fields."""
    new_company = GlobalCompanies(
        gc_id=generate_random_gc_id(),
        name=name,
        url=url if url else "Unknown",
        mm_Companies=mm_companies,
        image=image,
        city=city if city else "Unknown",
        state=state if state else "Unknown",
        country=country if country else "Unknown",
        size=size if size else "Unknown",
        sector=sector if sector else "Unknown", 
        p_and_l_category=p_and_l_category if p_and_l_category else "Unknown", 
        p_and_l_subcategory=p_and_l_subcategory if p_and_l_subcategory else "Unknown", 
    )
    new_company.save()

    if mm_company_list:
        for mm_company in mm_company_list:
            new_company.mm_companies.add(mm_company)  # Add the mmCompanies instances to the GlobalCompanies instance

    return new_company

    def __str__(self):
        return self.name
