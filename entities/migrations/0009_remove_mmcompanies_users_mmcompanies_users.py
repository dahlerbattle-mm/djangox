# Generated by Django 5.0.3 on 2024-04-26 23:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0008_alter_mmcompanies_url'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mmcompanies',
            name='users',
        ),
        migrations.AddField(
            model_name='mmcompanies',
            name='users',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]