from django.contrib import admin
from .models import OAuthCredentials


class OAuthCredentialsAdmin(admin.ModelAdmin):
    # TODO: this isn't working right
    list_display = ("user", "service", "access_token", "refresh_token", "created_at", "expiration_at")


admin.site.register(OAuthCredentials, OAuthCredentialsAdmin)