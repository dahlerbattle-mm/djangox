# Generated by Django 5.0.3 on 2024-05-07 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0004_oauthcredentials_realm_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthcredentials',
            name='last_api_pull_at',
            field=models.DateTimeField(null=True),
        ),
    ]
