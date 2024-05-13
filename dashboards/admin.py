from django.contrib import admin
from django.conf import settings
from .models import DashboardData
from accounts.models import Profile  # Assuming Profile is in the same models.py

class DashboardDataAdmin(admin.ModelAdmin):
    """Admin view of json data in DashboardData model"""
    list_display = ('user', 'source', 'category', 'display_payload', 'display_clean_payload', 'created_at', 'updated_at')

    def display_payload(self, obj):
        # Check if the payload is not empty
        if obj.payload:  # This checks if clean_payload is not None or not an empty string/dictionary/list
            return True
        else:
            return False

    def display_clean_payload(self, obj):
        # Check if the payload is not empty
        if obj.clean_payload:  # This checks if clean_payload is not None or not an empty string/dictionary/list
            return True
        else:
            return False

admin.site.register(DashboardData, DashboardDataAdmin)


