from django.db import models



from django.contrib.auth.models import User

class UserIdentity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    public_key = models.TextField()
    # Add other identity attributes as needed




class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    address = models.CharField(max_length=255)
    private_key = models.CharField(max_length=255)
    ethereum_address = models.CharField(max_length=42, unique=True,null=True,blank=True)

    def __str__(self):
        return f"Wallet for {self.address}"
    


class SharedData(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_data')
    recipient = models.CharField(max_length=100)  # Assuming recipient address as a string
    encrypted_message = models.TextField(null=True, blank=True, max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shared data from {self.sender.username} to {self.recipient}"