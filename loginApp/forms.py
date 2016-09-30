from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import  UserProfile



class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Username.")
    email = forms.CharField(help_text="Email Address.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    
    idno = forms.CharField(help_text="National Id Number.", required=False)
    photo = forms.ImageField(help_text="Upload Profile Image.", required=False)
    description = forms.CharField(help_text=" More about you/description.", required=False)
    class Meta:
        model = UserProfile
        fields = ('idno', 'photo','description')
