# Generated by Django 5.0.3 on 2024-04-25 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_id',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]