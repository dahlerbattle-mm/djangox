from django.contrib import admin
from .models import OAuthCredentials


class OAuthCredentialsAdmin(admin.ModelAdmin):
    """Admin View of OAuth Credentials Information"""
    list_display = ("user", "service", "access_token", "refresh_token", "realm_id", "created_at", "expiration_at", "last_api_pull_at")


admin.site.register(OAuthCredentials, OAuthCredentialsAdmin)