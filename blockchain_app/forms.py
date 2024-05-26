from django import forms
from .models import UserIdentity

class UserIdentityForm(forms.ModelForm):
    class Meta:
        model = UserIdentity
        fields = ['name', 'public_key']
        # Add other fields as needed


from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    pass
