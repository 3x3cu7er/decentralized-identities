from django import forms
from .models import File

# Name are automatically made for each field if we dont assign any. (they are used to connect with name in html)
# (so it know which field the dat should go to)
# converted html
class UploadFileForm(forms.ModelForm):
    fileName = forms.CharField(required=True, label="File Name")
    fileDir = forms.FileField(required=True, label="File")

    class Meta:
        model = File # link
        fields = ['fileName', 'fileDir'] # what will be in the form (attributes)

