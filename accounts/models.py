from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import random

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.email

# Profile Model
class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_id = models.CharField(max_length=100, unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    s3_url = models.URLField(max_length=200, blank=True, null=True)
    profile_pic_url = models.URLField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.profile_id:  # Generate profile_id only if it's not already set
            self.profile_id = self._generate_unique_profile_id()
        super().save(*args, **kwargs)
    
    def _generate_unique_profile_id(self):
        while True:
            potential_id = "p_id" + str(random.randint(100000, 999999))  # Generate a random number between 100000 and 999999
            if not Profile.objects.filter(profile_id=potential_id).exists():
                return potential_id

    def __str__(self):
        return f'{self.user.username} Profile'