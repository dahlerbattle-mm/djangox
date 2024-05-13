from django.contrib import admin
from .models import ContactUs

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'category', 'message')
    search_fields = ('user_id', 'category')

