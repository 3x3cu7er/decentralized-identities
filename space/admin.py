from django.contrib import admin
from .models import FileDrive,Profile,PasswordOTP,CredentialsDrive
# Register your models here.

admin.site.register(FileDrive)
admin.site.register(Profile)
admin.site.register(PasswordOTP)
admin.site.register(CredentialsDrive)
