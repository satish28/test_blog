from django import forms
from django.contrib.auth.models import User 


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=15, help_text="Firstname")
    last_name = forms.CharField(max_length=15, help_text="Lastname")
    email = forms.EmailField(help_text='Email ID')
    password = forms.CharField(widget=forms.PasswordInput, max_length=15, help_text="Password")
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')