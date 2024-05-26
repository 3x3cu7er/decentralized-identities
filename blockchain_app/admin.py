from django.contrib import admin
from .models import SharedData,Wallet,UserIdentity
# Register your models here.
admin.site.register(SharedData)
admin.site.register(Wallet)
admin.site.register(UserIdentity)
