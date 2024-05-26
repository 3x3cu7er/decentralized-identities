from django.contrib import admin

# Register your models here.
from .models import IdentityManager

admin.site.register(IdentityManager)