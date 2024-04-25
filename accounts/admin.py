from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileForm
from .models import CustomUser, Profile

# User admin interface
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]

admin.site.register(CustomUser, CustomUserAdmin)

# Profile admin interface
class ProfileAdmin(admin.ModelAdmin):
    # add_form = N/A
    form = ProfileForm
    model = Profile
    list_display = ['profile_id', 'first_name', 'last_name', 'title', 'created_at',]

# Register the admin class with the associated model
admin.site.register(Profile, ProfileAdmin)
