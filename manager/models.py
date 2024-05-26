from django.db import models
from django.contrib.auth.models import User

class Identifier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    did = models.CharField(max_length=255, unique=True)

class VerifiableCredential(models.Model):
    did = models.CharField(max_length=255,null=True,blank=True)
    credential_type = models.CharField(max_length=100,null=True,blank=True)
    issuer = models.CharField(max_length=255,null=True,blank=True)
    credential_data = models.TextField(null=True, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)
#