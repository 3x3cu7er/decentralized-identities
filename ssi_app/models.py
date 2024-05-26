from django.db import models

class Identity(models.Model):
    user_address = models.CharField(max_length=42, unique=True)  # Ethereum address
    user_name = models.CharField(max_length=100,null=True, blank=True)
    ipfs_hash = models.CharField(max_length=46, unique=True,null=True,blank=True)  # IPFS hash
