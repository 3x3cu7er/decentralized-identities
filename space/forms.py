from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','last_name','first_name','email','password']
 
        



class ProfileUpdateForm(ModelForm):
    class Meta:
        
        model = Profile
        fields = ['image']
        
    