# identities/models.py

from django.db import models
from django.contrib.auth.models import User

class Identity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    ipfs_hash = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name

class IPFSData(models.Model):
    user_ipfs_hash = models.CharField(max_length=255,null=True, blank=True)
    ipfs_hash = models.CharField(max_length=255,null=True, blank=True)
    data_description = models.CharField(max_length=255,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    
    def __str__(self):
        return self.data_description
    


class DecentralizedIdentifier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    did = models.CharField(max_length=255, unique=True)

class VerifiableCredential(models.Model):
    did = models.ForeignKey(DecentralizedIdentifier, on_delete=models.CASCADE)
    credential = models.TextField()
    issued_at = models.DateTimeField(auto_now_add=True)