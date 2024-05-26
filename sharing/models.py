from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .fileManagement import user_directory_path

class File(models.Model):
    fileName = models.CharField(max_length=255)
    fileSize = models.FloatField()
    fileType = models.CharField(max_length=10, null=True)
    # we dont use () so upload_to can call only when needed.
    fileDir = models.FileField(null=True, upload_to=user_directory_path) # upload_to calls the fun automatically with 2 argumnets (File object and filename)
    fileHash = models.CharField(max_length=64) #sha-256
    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='ownedFiles')
    # shared attributes
    shared = models.BooleanField(default=False)
    #relaed_name is used for reverse relation. owned_files = user.ownedFiles.all() 
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, default=False, related_name='sharedFiles')
    
    created_shared_at = models.DateTimeField(default=timezone.now)

    # self is the file it self we copying:
    def make_share_file(self, recipient):
        # if not self.shared and recipient != self.owner:
        if recipient != self.owner:
            # Create a new instance for the recipient user
            shared_file = File.objects.create(
                fileName=self.fileName,
                fileSize=self.fileSize,
                fileType=self.fileType,
                #fileDir=user_directory_path(), 
                fileHash=self.fileHash,  
                owner=recipient,
                shared=True,
                sender=self.owner,
                created_shared_at=timezone.now(),
            )

            return shared_file
        

    
    def __str__(self):
        return self.fileName
    
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(fileSize__gte=0.0), name='file_size_non_negative_check'),
        ]

        

import datetime

class ShareData(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_texts_owned')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_texts_received')
    created_at = models.DateTimeField(blank=True,null=True,auto_now=True)
    time_limit = models.DateTimeField(blank=True,null=True)
    def __str__(self):
        return f"{self.owner}"
    
    def is_expired(self):
        if self.time_limit is None:
            return False  # No expiration if time_limit is not set
        return timezone.now() > self.created_at + self.time_limit



from django.db import models

class PrivateKey(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    private_key_text = models.TextField()

class EncryptedData(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    private_key = models.ForeignKey(PrivateKey, on_delete=models.CASCADE)
    encrypted_text = models.BinaryField()
