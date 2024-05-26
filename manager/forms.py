from django import forms

class CreateDIDForm(forms.Form):
    did = forms.CharField(max_length=255)

class IssueCredentialForm(forms.Form):
    did = forms.CharField(max_length=255)
    credential_data = forms.CharField(widget=forms.Textarea)

from .models import VerifiableCredential

class UpdateCredentialForm(forms.ModelForm):
    class Meta:
        model = VerifiableCredential
        fields = ['credential_type', 'issuer', 'credential_data']  # Adjust fields as needed
