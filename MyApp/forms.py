from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import Complaint
from .models import User
from django.contrib.auth.forms import UserChangeForm
from .models import UserProfile


class RegistrationForm(UserCreationForm):
    # mobile = forms.CharField(max_length=15, required=True, label='Mobile Number')
    # address = forms.CharField(widget=forms.TextInput, required=True, label='Address')
    password1 = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, label='Confirm Password', widget=forms.PasswordInput)
    username = forms.CharField(label='Name', widget=forms.TextInput, required=True)

    class Meta:
        model = User  # Use your custom user model
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = '' 

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['mobile', 'address']


class ComplaintForm(forms.ModelForm):  
    class Meta:
        model = Complaint
        fields = ['name', 'place', 'Description', 'PhysicalEvidence', 'fileUpload']
        widgets ={'user':forms.HiddenInput}

from .models import Criminal

class CriminalForm(forms.ModelForm):
    class Meta:
        model = Criminal
        fields = ['name', 'photo', 'description']