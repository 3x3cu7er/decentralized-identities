from db_connect import file_db,account_db,credential_db
from django.contrib.auth.models import User
from PIL import Image
file_collection  = file_db['File']
acoount_collection = account_db['UserAccount']
credential_collection = credential_db['Credentials']

from django.db import models


class FileDrive(models.Model):
    auto_increment_id = models.AutoField(primary_key=True,default=1)
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    file = models.FileField(upload_to='Drive')
    file_tag = models.CharField(max_length= 255, null=True)
    # file_stored_on_ipfs = models.FileField(storage=InterPlanetaryFileSystemStorage())

    def __str__(self):
        return str(self.created)

    # class Meta:
    #     order_with_respect_to = 'user'


class CredentialsDrive(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    id_name = models.CharField(max_length=200,null=True)
    given_name = models.CharField(max_length= 200,null=True)
    userAddress = models.TextField(max_length= 200,null=True)
    description = models.TextField(blank=True)
    body = models.TextField(max_length= 200,null=True)
    
    def __repr__(self):
        return self.id_name
    
    

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pics",default="default.jpg")
    
    
    def __str__(self):
        return f"{self.user.username} Profile"
    
    def save(self):
        super().save()
        
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
            
    
class PasswordOTP(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, null=True, blank=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} OTP generated on {self.created_at}"
    
