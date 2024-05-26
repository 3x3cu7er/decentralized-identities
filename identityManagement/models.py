from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class IdentityManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    ethereum_address = models.CharField(max_length=42, unique=True,null=True,blank=True)
    name = models.CharField(max_length=255,blank=True,null=True)
    email = models.CharField(max_length=255,null=True,blank=True)
    verified = models.BooleanField(default=False)
    shared_data = models.JSONField(default=dict,null=True, blank=True)
    data_expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
