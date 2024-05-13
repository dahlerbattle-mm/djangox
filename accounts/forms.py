from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile

class CustomUserCreationForm(UserCreationForm):
    """Form to create a CustomUser"""
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username',)

class CustomUserChangeForm(UserChangeForm):
    """Form to edit a CustomUser"""
    class Meta:
        model = CustomUser
        fields = ('email', 'username',)

class ProfileForm(forms.ModelForm):
    """Form to create a profile for a CustomUser"""
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'title']