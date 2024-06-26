# Generated by Django 5.0.3 on 2024-04-25 17:38

import django.contrib.postgres.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='mmCompanies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mmc_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True, null=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('size', models.CharField(choices=[('0-9', 'SME'), ('10-49', 'SME'), ('50-99', 'Lower Middle Market'), ('100+', 'Upper Middle Market')], max_length=100)),
                ('sector', models.CharField(choices=[('information_technology', 'Information Technology'), ('consumer_discretionary', 'Consumer Discretionary'), ('communication_services', 'Communication Services'), ('unknown', 'Unknown'), ('financials', 'Financials'), ('healthcare', 'Healthcare'), ('energy', 'Energy'), ('consumer_staples', 'Consumer Staples'), ('materials', 'Materials'), ('industrials', 'Industrials'), ('utilities', 'Utilities'), ('real_estate', 'Real Estate')], max_length=100)),
                ('s3_url', models.URLField(blank=True, null=True)),
                ('quartile1_price', models.IntegerField(blank=True, null=True)),
                ('quartile2_price', models.IntegerField(blank=True, null=True)),
                ('quartile3_price', models.IntegerField(blank=True, null=True)),
                ('quartile4_price', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('users', models.ManyToManyField(related_name='companies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalCompanies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gc_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True, null=True)),
                ('image', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('size', models.CharField(choices=[('0-9', 'SME'), ('10-49', 'SME'), ('50-99', 'Lower Middle Market'), ('100+', 'Upper Middle Market')], max_length=100)),
                ('sector', models.CharField(choices=[('information_technology', 'Information Technology'), ('consumer_discretionary', 'Consumer Discretionary'), ('communication_services', 'Communication Services'), ('unknown', 'Unknown'), ('financials', 'Financials'), ('healthcare', 'Healthcare'), ('energy', 'Energy'), ('consumer_staples', 'Consumer Staples'), ('materials', 'Materials'), ('industrials', 'Industrials'), ('utilities', 'Utilities'), ('real_estate', 'Real Estate')], max_length=100)),
                ('p_and_l_category', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('cogs', 'COGS'), ('g&a', 'G&A'), ('s&m', 'S&M'), ('d&a', 'D&A'), ('r&d', 'R&D'), ('interest', 'Interest'), ('non_operating_income', 'Non Operating Income'), ('non_operating_expense', 'Non Operating Expense'), ('taxes', 'Taxes')], max_length=100), default=list, size=None)),
                ('p_and_l_subcategory', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('product_income', 'Product Income'), ('service_income', 'Service Income'), ('subscription_income', 'Subscription Income'), ('royalty_income', 'Royalty Income'), ('other_income', 'Other Income'), ('materials', 'COGS - Materials'), ('direct_labor', 'COGS - Direct Labor'), ('manufacturing_supplies', 'COGS - Manufacturing Supplies'), ('production_overhead', 'COGS - Production Overhead'), ('office', 'G&A - Office'), ('g&a_salaries', 'G&A - Salaries'), ('rent_lease', 'G&A - Rent & Lease'), ('utilities', 'G&A - Utilities'), ('misc.', 'G&A - Misc.'), ('r&d_salaries.', 'R&D - Salaries'), ('product_development', 'R&D - Product Development'), ('software_development', 'R&D - Software Development'), ('s&m_salaries', 'S&M - Salaries'), ('s&m_software', 'S&M - Software'), ('s&m_advertising', 'S&M - Advertising'), ('s&m_commisions', 'S&M - Commisions'), ('county_taxes', 'Taxes - County'), ('state_taxes', 'Taxes - State'), ('federal_taxes', 'Taxes - Federal'), ('sale_of_assets', 'Non-Operating - Sale of Asset Gain/Loss'), ('fx_gain_loss', 'Non-Operating - Foreign Exchange Gain/Loss'), ('investment_income', 'Non-Operating - Investment Income Gain/Loss'), ('grant', 'Non-Operating - Grant Income')], max_length=100), default=list, size=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mm_Companies', models.ManyToManyField(related_name='mm_companies', to='entities.mmcompanies')),
            ],
        ),
    ]
