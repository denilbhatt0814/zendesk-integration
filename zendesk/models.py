from django.db import models
from django.utils import timezone

# # Create your models here.
class AccessToken(models.Model):
    token = models.CharField(max_length=200)
    subdomain = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)