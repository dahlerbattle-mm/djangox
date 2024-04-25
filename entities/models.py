from django.db import models
from django.conf import settings
from accounts.models import CustomUser
from django.contrib.postgres.fields import ArrayField

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
    # Relationship to User model
    mmc_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=200, blank=True, null=True)
    users = models.ManyToManyField(CustomUser, related_name='companies')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    size = models.CharField(max_length=100, choices=SIZE_CHOICES)
    sector = models.CharField(max_length=100, choices=SECTOR_CHOICES)
    s3_url = models.URLField(max_length=200, blank=True, null=True)
    quartile1_price = models.IntegerField(blank=True, null=True)
    quartile2_price = models.IntegerField(blank=True, null=True)
    quartile3_price = models.IntegerField(blank=True, null=True)
    quartile4_price = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.mmc_id:  # Generate profile_id only if it's not already set
            self.mmc_id = self._generate_unique_mmc_id()
        super().save(*args, **kwargs)
    
    def _generate_unique_mmc_id(self):
        while True:
            potential_id = "mmc_" + str(random.randint(100000, 999999))  # Generate a random number between 100000 and 999999
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
    size = models.CharField(max_length=100, choices=SIZE_CHOICES)
    sector = models.CharField(max_length=100, choices=SECTOR_CHOICES)
    p_and_l_category = ArrayField(models.CharField(max_length=100, choices=P_AND_L_CATEGORY_CHOICES), default=list)
    p_and_l_subcategory = ArrayField(models.CharField(max_length=100, choices=P_AND_L_SUBCATEGORY_CHOICES), default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
