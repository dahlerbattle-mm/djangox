from django.db import models
from django.conf import settings

SERVICE_CHOICES = [
    (service['name'], service['name']) for service in settings.INTEGRATION_SERVICES
]


class OAuthCredentials(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.CharField(max_length=500)
    access_token = models.TextField(max_length=500)
    refresh_token = models.TextField(max_length=500)
    expiration_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
