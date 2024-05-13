# Generated by Django 5.0.3 on 2024-05-08 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0002_dashboarddata_source_alter_dashboarddata_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboarddata',
            name='category',
            field=models.CharField(blank=True, choices=[('revenue', 'Revenue'), ('expenses', 'Expenses'), ('p&l', 'P&L'), ('balance_sheet', 'Balance Sheet'), ('customers', 'Customers'), ('deals', 'Deals'), ('product', 'Product'), ('services', 'Services'), ('hr', 'HR')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='dashboarddata',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]