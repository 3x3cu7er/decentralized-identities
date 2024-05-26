from django import forms
from .models import IdentityManager

class IdentityForm(forms.ModelForm):
    class Meta:
        model = IdentityManager
        fields = ['ethereum_address', 'name', 'email']
