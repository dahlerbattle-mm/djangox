# Generated by Django 5.0.3 on 2024-04-26 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0006_alter_globalcompanies_sector_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalcompanies',
            name='sector',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='globalcompanies',
            name='size',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]